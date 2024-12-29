from PyQt5.QtWidgets import QApplication, QLabel, QStyleFactory

print(QStyleFactory.keys())

app = QApplication([])
QApplication
label = QLabel('Hello World!')
label.show()
app.exec_()


