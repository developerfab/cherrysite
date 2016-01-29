import smtplib

def mensaje(msg):
    print msg
    fromaddr = 'parapruebasfab@gmail.com'
    toaddrs  = 'fab7696650@gmail.com'
    # Credentials (if needed)
    username = 'parapruebasfab@gmail.com'
<<<<<<< HEAD
    password = 'AFmedellin48'
=======
    password = ''
>>>>>>> a837b197a8bbcb8de1fcdd2892e6a3472195a2e4
    mensaje = '''\\
    From: parapruebasfab@gmail.com
    Subject: contacto

    '''
    mensaje = mensaje+"\n"+msg

    # The actual mail send
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(username,password)
    server.sendmail(fromaddr, toaddrs, mensaje)
    server.close()
