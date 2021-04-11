def sendEmail():
    import logging
    from logging.handlers import SMTPHandler
    from logging import Formatter

    mail_handler = SMTPHandler('smtp.bgu.ac.il',
                               'netbio@post.bgu.ac.il',
                               ['netbio@post.bgu.ac.il'], 'TRACE has failed')
    mail_handler.setLevel(logging.ERROR)

    mail_handler.setFormatter(Formatter('''
    Message type:       %(levelname)s
    Location:           %(pathname)s:%(lineno)d
    Module:             %(module)s
    Function:           %(funcName)s
    Time:               %(asctime)s

    Message:

    %(message)s
    '''))