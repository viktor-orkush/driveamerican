from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET


@require_GET
def robots_txt(request):
    lines = [
        "User-agent: Googlebot\n",
        "User-agent: *\n",
        "Disallow: /admin/\n",
        "Sitemap: http://driveamerican.top/sitemap.xml\n",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


def sitemap_xml(request):
    return render(request, 'sitemap.xml')
