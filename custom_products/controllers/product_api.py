# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http
from odoo.http import request


class ProductApiController(http.Controller):

    
    # Produce Search
    @http.route('/get/product_list', type='json', auth="none")
    def get_product_list(self, **kw):
        if request.httprequest.method == 'POST':
            product_list = []
            product_search = request.env['product.template'].sudo().search([])
            for p in product_search:
                product_list.append({
                    "part": p.part,
                    "default_code": p.default_code,
                    "revision": p.revision,
                    "name": p.name,
                    "part_type":p.part_type,
                    "material": p.material,
                    "length": p.length,
                    "breadth": p.breadth,
                    "height": p.height,
                    "weight": p.weight,
                    "lifecycle_status": p.lifecycle_status
                })

            request.params['product_list'] = product_list
            return request.params
        
    # Product Delete
    @http.route('/api/product_delete/', type='json', auth="none")
    def product_delete_fun(self, **kw):
        if request.httprequest.method == 'POST':
            part_no = request.params['part_no']
            
            record = request.env['product.template'].sudo().search([('default_code','=',part_no)])
            for i in record:
                i.unlink()
        
    @http.route('/api/product_create/', type='json', auth="none")
    def producte_create(self, **kw):
        part = request.params['part']
        default_code = request.params['default_code']
        revision = request.params['revision']
        name = request.params['name']
        part_type = request.params['part_type']
        material = request.params['material']
        length = request.params['length']
        breadth = request.params['breadth']
        height = request.params['height']
        weight = request.params['weight']
        lifecycle_status = request.params['lifecycle_status']
        
        p_search_obj = request.env['product.template'].sudo().search([('default_code','=',default_code)])
        product_Categ_id = request.env['product.category'].sudo().search([('name','=','All')],limit=1)
        if not p_search_obj:           
            request.env['product.product'].sudo().create({
                "part": part,
                "default_code": default_code,
                "revision": revision,
                "name": name,
                "part_type":part_type,
                "material": material,
                "length": length,
                "breadth": breadth,
                "height": height,
                "weight": weight,
                "lifecycle_status": lifecycle_status,
#                 'categ_id':product_Categ_id,
#                 'company_id':company_id,
#                 'uom_id':1,
#                 'uom_po_id':1,
#                 'sale_line_warn':company_id.id,
#                 'uom_id':company_id.id,
#                 'uom_po_id':company_id.id,
#                 'company_id':company_id.id,
            })
            request.params['status'] = 'Product Created Successfully'
        else:
            request.params['status'] = 'Product Name already Exists'
        return request.params
            
            
            