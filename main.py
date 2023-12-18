import time
import media_processor
import translator
import media_downloader

import telemetry


def main(title):
    print(title)

    processor = media_processor.MediaProcessor(
        '123',
        '001'
    )

    vd_options = {
        'url': 'https://www.youtube.com/watch?v=Fx1Qp_a-OBI',
        'video_filename': 'video1.mkv',
    }
    processor.video_download_node(vd_options)

    vtta_options = {
        'video_filename': 'video1.mkv',
        'source_language': 'en',
        'target_language': 'es',
        'level': 'low'
    }
    processor.video_to_translated_audio_node(vtta_options)

    # to be able to actually translate a text completely we need to introduce pauses and
    # split the text using those pause symbols

    # timer = telemetry.Telemetry()
    # transcription = {'text': 'Bienvenido a metabolismotv tu fuente de información correcta sobre metabolismo y la salud. El cáncer es frío. Yo soy Frank Suárez especialista en publicidad de metabolismo y quiero compartir contigo una información que tiene que ver con el tema del cáncer. Ultimamente ha estado envuelto con el tema de la investigación del cáncer porque estoy trabajando con un libro que se llama si yo tuviera cáncer, donde básicamente pongo toda la ciencia que conozco y qué cosas se recomendarían desde el punto de vista científico, el punto de vista práctico para hacer si uno quisiera evitar un cáncer. Ayudar a alguien con cáncer, ese tipo de cosa no este uno de los temas es que descubro que el cáncer definitivamente es frío. Les explico un momentito ahora la pizarra es él el tema pocas cosas traen tantas emociones negativas tantas emociones de terror de miedo de incertidumbre como un diagnóstico de cáncer que este nada va a hacer sentir más y según una persona que un diagnóstico de eso este puede ser devastador. Entonces siempre para mí yo pienso mi punto de vista es que yo prefiero siempre saber lo más que pueda sobre aquello que tengo que conformar que confrontar no es así yo tengo un problema en frente a mí me gustaría saber lo más posible sobre ese que compone eso porque mientras más yo sepa más yo sepa sus componentes o factores los distintos factores que afectan ese problema o que lo crean más oportunidades yo tengo que resolverlo por lo menos ese es mi punto de vista entonces algo que debes saber es que el cáncer las células cancerosas cáncer es frío quiere decir que es una temperatura baja porque piense las células del cuerpo son así que dentro de la célula pues hay una parte que se llama la mitocondria de hecho yo siempre le dibujo como si fuera una sola, pero la verdad es que una célula puede tener de mil a dos mil mitocondrias, pero para efecto de discusión esa parte que se llama la mitocondria es donde penetran los carbohidratos en forma de glucosa la proteína en forma de aminoácido lo la grasa y aceite que es un lípido en forma de gravita y aceite aquí y aquí también es que entra el oxígeno cuando hay combustible que sería carbohidrato proteína grasa aceite y hay oxígeno pues entonces hay combustión cuando hay combustión pues la combustión que es como un fueguino va a producir calor su cuerpo está calentito está calentito porque usted está vivo o viva este si te toca una persona bien envejecida bien envejeciendo que está bien enfermizo lo vas contra el frío de hecho cuando usted toca un paciente de cáncer lo va a contar bien frío la temperatura de un paciente de cáncer siempre feria a menos que esté pasando por un momento de fiebre, pero generalmente la temperatura del paciente canceroso es fría y fría porque su cuerpo no está pudiendo producir suficiente energía ahora el cáncer es frío y qué cosa se puede hacer con eso es si usted sabe que frío usted sabe que el cáncer tiene que ver con la falta de energía ya el doctor Otto carburo ganador del premio nobel allá en el año mil novecientos veintiséis ganó un premio nobel porque descubrió y pudo comprobar que para tener cáncer primero había que restar el oxígeno él le dieron su premio nobel porque si usted les restaba el treinta y cinco probó que si le restaba el treinta y cinco por ciento del oxígeno una célula la volvía cancerosa una célula saludable la unidad cancerosa entonces qué pasa el cáncer tiene que ver con la falta de energía es un problema metabólico realmente no le han echado la culpa del cáncer a lo genético a los genes y todo tipo cosa, pero en verdad es una situación de falta de energía cuando usted se acerca a un paciente cáncer o solo base que está frío lo vas a etiqueta frío la salud tiene que ver con el calorcito con el movimiento te toma un bebé recién nacido en sus brazos babel que está bien calentito se le acercó una persona bien en Facebook que si está bien debería bastar bien debido a que se pueda ser y por qué es que muchas de las terapias que recomienda para el cáncer tienen que ver con calor se ha visto que por ejemplo si hay un tumor canceroso y ponen rayos infrarrojos los rayos infrarrojos penetran la piel y causan calor y eso empieza a reducir el tumor y eso se ha podido comprobar si una de las terapias que recomiendan para la persona que tiene un cáncer es ponerle calor que se ha visto también que los baños termales como agua caliente agua termal también tiene la tendencia a reducir los tumores porque el cáncer de por sí es frío, pero es frío porque no tiene energía no crea energía la célula cancerosa en vez de oxidar lo que hace es que fermenta las células cancerosas solamente usan glucosa azúcar no pueden comer no pueden utilizar la grasa el aceite no pueden usar las proteínas las células cancerosas solamente usan glucosa el cáncer de hecho es una célula supertragona de glucosa por eso la peor forma se ha podido demostrar que si se mantiene la glucosa muy alta, pero si la persona come mucho chocolate dulce pan harina lo que sea mientras tiene un cáncer lo que hace que solo se crece así que si usted tiene un paciente un ser querido con cáncer por favor no le lleve galletita no le lleve pan no le lleve chocolate no lo lleve dulce porque lo que hace es echarle eso es como echarle gasolina al fuego así que básicamente el cáncer es frío, por lo tanto, todo lo que sea aumentar calor tiende a reducir el cáncer qué cosas pueden hacerlo pueden hacer un baño termal puede hacerlo a infrarrojo puede hacerlo tomar agua te toma suficiente agua el agua aumenta la energía que se llama ATP en las células y aumenta el calor y lo otro que lo hace es tomar el sol que si has visto que el tomar el sol crea vitamina y la vitamina se aumenta la energía de la célula además anti cáncer así que cuando usted piense en alguien con cáncer piensen está frío hay que aumentar el calor y unas recomendaciones básicas para evitar el cáncer es manejar estas cosas como baño termal infrarrojo sol suficiente agua para que se cree suficiente energía para que haya calorcito la vida tiene que ver con el calor tiene que ver con el movimiento las cosas vivas se mueven las cosas muertas no se mueven así que a la hora de mirar un cáncer o de evitarlo piense en que su cuerpo necesita calor el sol es bueno el agua y bueno los rayos infrarrojos un bono para calentar el cuerpo y los baños termales también lo son y esto se los comento porque la verdad siempre triunfa.'}
    # transcription = processor.correct_transcription(transcription, 'es', timer, 0)
    # print(transcription)
    #
    # translation = processor.translate(
    #     transcription,
    #     timer,
    #     100
    # )
    # print(translation)


if __name__ == '__main__':
    main('Welcome to AudioMaster!')
