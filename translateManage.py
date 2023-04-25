from googletrans import Translator
translator = Translator(service_urls=['translate.googleapis.com'])

local_language = {
  "Amharic": "am",
  "Arabic": "ar",
  "English": "en",
  "Somali": "so",
  "Afan Oromo": "om",
  "Tigrinya": "ti"

}


def find_lan(language_code):
  key_value = list(local_language.keys())
  try :
    value = list(local_language.values()).index(language_code)
    return key_value[value]
  except :
    return None


def traslatedMessage(message , dest):
  try :
    result = translator.translate(message, dest)
    is_local_language = find_lan(result.src)
    if is_local_language:
      return find_lan(result.src), find_lan(result.dest) , result.origin ,result.text
    else:
      print("We only translate local languages")

  except:
    print("Error Occur during Translation")


if __name__ == '__main__':
  message = ""
  source , destination , originalMessage ,transMessage = traslatedMessage(message , local_language['Amharic'])
  print("This Text is translated from : ", source, " to ", destination)
  print("Original Text :", originalMessage)
  print("Translated Text :", transMessage)


