import email
import wave

message = email.message_from_file(open('message.txt'))
attachment = message.get_payload()[0]
open('indian.wav', 'wb').write(attachment.get_payload(decode=True))

original_wav = wave.open('indian.wav', 'rb')

reversed_wav = wave.open('reversed_indian.wav', 'wb')
reversed_wav.setparams(original_wav.getparams())
for frame in range(original_wav.getnframes()):
    reversed_wav.writeframes(original_wav.readframes(1)[::-1])
reversed_wav.close()

print "Done :)"
