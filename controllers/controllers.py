# -*- coding: utf-8 -*-
from odoo import http

# class BookingOrderReziva05042001(http.Controller):
#     @http.route('/booking_order_reziva_05042001/booking_order_reziva_05042001/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/booking_order_reziva_05042001/booking_order_reziva_05042001/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('booking_order_reziva_05042001.listing', {
#             'root': '/booking_order_reziva_05042001/booking_order_reziva_05042001',
#             'objects': http.request.env['booking_order_reziva_05042001.booking_order_reziva_05042001'].search([]),
#         })

#     @http.route('/booking_order_reziva_05042001/booking_order_reziva_05042001/objects/<model("booking_order_reziva_05042001.booking_order_reziva_05042001"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('booking_order_reziva_05042001.object', {
#             'object': obj
#         })