#!/usr/bin/env python

import binascii
import os
import re
import sys

from PyQt5 import QtCore, QtWidgets
import pycoin.key
import requests

from hec.encryption import decode_point, encrypt, decrypt
from hec.gui import Ui_MainWindow


# Returns a point
def search_for_pubkey(address):
    # Do this in order to raise an pycoin.encoding.EncodingError if necessary.
    pycoin.key.Key.from_text(address)

    response = requests.get('https://blockchain.info/q/pubkeyaddr/' + address)

    pubkey_hex = response.text
    if len(pubkey_hex) < 16:
        raise Exception("Pubkey not found")

    return decode_point(binascii.unhexlify(pubkey_hex))


# Returns the secret.
def load_secret_from_wallet_dat(address, statusBar=None):
    if 'HOME' in os.environ:
        path = os.environ['HOME'] + "/.bitcoin"
    path = QtWidgets.QFileDialog.getOpenFileName(None, 'open wallet.dat', path)[0]
    with open(path, "rb") as f:
        wallet = f.read()
    priv_keys = set(re.findall(b'\x70\x6F\x6F\x6C(.{52})', wallet))
    total = len(priv_keys)
    for index, key in enumerate(priv_keys):
        statusBar.showMessage("Searched " + str(index) + "/" + str(total) + " privkeys")
        QtCore.QCoreApplication.processEvents()
        secret = int.from_bytes(key[20:], 'big')
        key = pycoin.key.Key(secret_exponent=secret)
        if key.address() == address:
            return secret
    raise Exception("Secret exponent not found")


def handle_encrypt(ui):
    try:
        ui.statusBar.showMessage("Searching...")
        pub_point = search_for_pubkey(ui.address.text())
    except Exception as e:
        ui.statusBar.showMessage("Error: " + str(e), 3000)
        return
    ui.statusBar.showMessage("Encrypting...")
    ui.message.setPlainText(encrypt(pub_point, ui.message.toPlainText()))
    ui.statusBar.showMessage("Encrypted.")


def handle_decrypt(ui):
    if ui.secret_exponent.text():
        secret = binascii.unhexlify(ui.secret_exponent.text())
    else:
        if not ui.address.text():
            ui.statusBar.showMessage("Error: Need address or secret exponent.", 3000)
            return

        try:
            ui.statusBar.showMessage("Searching...")
            secret = load_secret_from_wallet_dat(ui.address.text(),ui.statusBar)
            ui.statusBar.clearMessage()
        except Exception as e:
            ui.statusBar.showMessage("Error: " + str(e), 3000)
            return

        ui.statusBar.showMessage("Decrypting...")
        try:
            plaintext = decrypt(secret, ui.message.toPlainText())
            ui.message.setPlainText(plaintext)
            ui.statusBar.showMessage("Decrypted.")
        except:
            ui.statusBar.showMessage("Invalid ciphertext.", 3000)

app = QtWidgets.QApplication(sys.argv)

class MyWindow(QtWidgets.QMainWindow):
    def mousePressEvent(self, event):
        self.mpos = event.pos()
    def mouseMoveEvent(self, event):
        if hasattr(self, 'mpos') and self.mpos:
            diff = event.pos() - self.mpos
            self.move(self.pos() + diff)
    def mouseReleaseEvent(self, event):
        self.mpos = None

mainWindow = MyWindow()
ui = Ui_MainWindow()
ui.setupUi(mainWindow)
mainWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint)
mainWindow.show()

ui.encrypt.clicked.connect(lambda: handle_encrypt(ui))
ui.decrypt.clicked.connect(lambda: handle_decrypt(ui))
ui.quit.clicked.connect(lambda: mainWindow.close())

sys.exit(app.exec_())

