# -*- coding: utf-8 -*-
# from odoo import http


# class Mangadex(http.Controller):
#     @http.route('/mangadex/mangadex/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mangadex/mangadex/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('mangadex.listing', {
#             'root': '/mangadex/mangadex',
#             'objects': http.request.env['mangadex.mangadex'].search([]),
#         })

#     @http.route('/mangadex/mangadex/objects/<model("mangadex.mangadex"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mangadex.object', {
#             'object': obj
#         })
