import speech_recognition as sr


def sphinx():
    # obtain audio from the microphone
    r = sr.Recognizer()
    harvard = sr.Microphone(device_index=0)
    # harvard = sr.AudioFile(r"voice (2).wav")
    with harvard as source:
        r.adjust_for_ambient_noise(source)
        audio = r.record(source)

    # recognize speech using Sphinx
    try:
        print("Sphinx thinks you said " + r.recognize_sphinx(audio, language='zh-cn'))
    except sr.UnknownValueError:
        print("Sphinx could not understand audio")
    except sr.RequestError as e:
        print("Sphinx error; {0}".format(e))



