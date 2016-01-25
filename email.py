from mailer import Mailer
from mailer import Message

message = Message(From="me@example.com",
                  To="fab7696650@gmail.com",
                  charset="utf-8")
message.Subject = "An HTML Email"
message.Html = """This email uses <strong>HTML</strong>!"""
message.Body = """This is alternate text."""

sender = Mailer('localhost')
sender.send(message)
