import email

message = email.message_from_file(open('message.txt'))
attachment = message.get_payload()[0]
open('indian.wav', 'wb').write(attachment.get_payload(decode=True))
