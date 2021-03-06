# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from models import Url
from django.views.decorators.csrf import csrf_exempt

import urllib


@csrf_exempt
def main_handler(request):
    response = ""
    # Compruebo con que método se ha enviado
    if request.method == "GET":
        # Escribo el formulario, la entrada y la cabecera de la lista
        entrada = "<p><b> Servidor acortador de URLs</b></p>\n\n\t\t"
        formulario  = '<FORM action="http://localhost:1234"'
        formulario += ' method="POST" accept-charset="UTF-8">\n\t\t'
        formulario += 'URL: <input type="text" name="url">\n\t\t'
        formulario += '     <input type="submit" value="Acortar">\n\t\t'
        lista = "</form>\n\n\t\t<p>Lista de URLs acortadas:</p>\n\t"
        # Saco todas las urls acortadas y muestro una por línea
        tabla = Url.objects.all()
        for fila in tabla:
            lista += "\t<p>" + "<a href='" + fila.url_larga + "'>"
            lista += fila.url_larga + "</a> ---> " + "<a href='"
            lista += fila.url_corta + "'>" + fila.url_corta + "</a></p>\n\t"
        # Escribo la respuesta en formato HTML
        response += "<html>\n\t<body>\n\t\t" + entrada + formulario + lista
        response += "</body>\n</html>\n"
        # Envío la respuesta
        HttpResponse.status_code = 200
        return HttpResponse(response)               
    elif request.method == "POST":
        # Busco el valor de contador
        if not Url.objects.all():
            # Si la base de datos esta vacía, contador sera 0
            contador = 0
        else:
            # En el resto de casos, sumo uno al valor de la ultima url acortada
            # Realizo esto para que funcione bien cuando se rearranque la app
            tabla = Url.objects.all()
            for fila in tabla:    
                url_corta = fila.url_corta
            contador = int(url_corta.split("/")[3]) + 1
        # Asigno a cuerpo la query string que nos envían por el POST
        cuerpo = request.body
        # Compruebo que la qs es correcta
        if len(cuerpo.split("=")) != 2 or cuerpo.split("=")[0] != "url":
            return HttpResponseNotFound("<html>\n\t<body>Error en el " +
                                        "formulario</body>\n</html>")
        # Me quedo con la url que viene en la qs
        url = cuerpo.split("=")[1]
        url = urllib.unquote(url).decode('utf8')
        # Si es necesario, añado "http://" a la url
        if url.split("://")[0] != "http" and url.split("://")[0] != "https":    
            url = "http://" + url
        # Compruebo si esa url ya ha sido acortada. Si no lo fue, la acorto y 
        # la guardo en la base de datos
        try:
            fila = Url.objects.get(url_larga=url)
            url_corta = fila.url_corta
        except Url.DoesNotExist:
            url_corta = "http://localhost:1234/" + str(contador)
            fila = Url(url_larga=url, url_corta=url_corta)
            fila.save()
        # Envío la respuesta
        response  = "<html>\n\t<body>\n\t\t<p><a href='" + url + "'>URL</a></p>"
        response += "\n\t\t<p><a href='" + url_corta + "'>URL Acortada</a>"
        response += "</p>\n\t</body>\n</html>\n"
        HttpResponse.status_code = 200
        return HttpResponse(response)
    else:
        # Si no es GET ni POST envío un mensaje de error
        return HttpResponseNotFound("<html>\n\t<body>Metodo erroneo</body>" + 
                                    "\n</html>")

def redirect_handler(request, recurso):
    if request.method == "GET":
        # Formulo la url acortada
        url_acortada = "http://localhost:1234/" + recurso
        print url_acortada
        # Compruebo si está en la base de datos
        try:
            fila = Url.objects.get(url_corta=url_acortada)
            url_larga = fila.url_larga
        except Url.DoesNotExist:
            # Si no está, envío un mensaje de error
            return HttpResponseNotFound("<html>\n\t<body>Recurso no " +
                                        "disponible</body>\n</html>")
        # Redirigo a la url real
        response  = '<html>\n\t<head><meta http-equiv="refresh" content="1; '
        response += 'url=' + url_larga + '" /></head>\n\t'
        response += '<body>Redirigiendo... </body>\n</html>'
        HttpResponse.status_code = 302
        return HttpResponse(response)
    else:
        # Si no es GET envío un mensaje de error
        return HttpResponseNotFound("<html>\n\t<body>Metodo erroneo</body>" + 
                                    "\n</html>")
