import pymysql


# Django espera el driver MySQLdb cuando se usa el backend mysql nativo.
# PyMySQL implementa esa interfaz en Python puro y esta línea lo registra
# antes de que Django abra conexiones con la base de datos.
pymysql.install_as_MySQLdb()
