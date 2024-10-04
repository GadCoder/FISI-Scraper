from transformers import pipeline

# Cargar el pipeline para resúmenes
resumidor = pipeline(
    "summarization", model="mrm8488/bert2bert_shared-spanish-finetuned-summarization"
)

# Texto que deseas resumir
texto = """
Se informa a los alumnos de la Facultad de Ingeniería de Sistemas e Informática, que aún no han recogido el carné universitario, pueden acercarse a la Unidad de Matrícula – FISI hasta el 15 de octubre del presente año, en horario de 8:00 a 13:00 y de 14:00 a 15:45 hrs.
NOTA IMPORTANTE:
• Los alumnos que no pueden asistir a recoger el carné, sírvanse otorgar una CARTA PODER SIMPLE a un familiar a fin de solicitar el mismo.
• Adjuntar copia de DNI de ambos.
Unidad de Matrícula, Registros Académicos, Grados y Títulos - FISI
"""

# Generar el resumen
resumen = resumidor(texto, max_length=50, min_length=25, do_sample=False)
print(resumen[0]["summary_text"])
