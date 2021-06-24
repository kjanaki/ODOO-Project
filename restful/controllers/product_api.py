# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http
from odoo.http import request
import json

class ProductApiController(http.Controller):

    # Access token get specified user
    def get_access_token(self, res_user_obj):
        if res_user_obj:
            return [i.token for i in res_user_obj.token_ids]

    # Product Search
    @http.route('/get/product_list', type='json', auth="public")
    def get_product_list(self, **kw):
        access_token = kw.get("access_token")
        res_user_obj = request.env['res.users'].sudo().search([('id','=',request.env.context['uid'])])
        acs_token_ids = self.get_access_token(res_user_obj)
            
#         access_token_rec = request.env['api.access_token'].sudo().search([('token','=',access_token)])
#         if access_token in access_token_rec.token:
        if access_token in acs_token_ids:
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
        else:
            return {"status": "error", "message": "Please provide 'Access Token' for this User %s"%res_user_obj.name}
        
    # Product Delete
    @http.route('/api/product_delete/', type='json', auth="public")
    def product_delete_fun(self, **kw):
        access_token = kw.get("access_token")
        res_user_obj = request.env['res.users'].sudo().search([('id','=',request.env.context['uid'])])
        acs_token_ids = self.get_access_token(res_user_obj)
        if access_token in acs_token_ids:
            if request.params.get('part_no'):
                part_no = request.params['part_no']
                record = request.env['product.template'].sudo().search([('default_code','=',part_no)])
                if record:
                    for i in record:
                        i.unlink()
                    return {"status":"sucess","message":"Products are deleted"}
                else:
                    return {"status":"sucess","message":"Product Part number not exist in 'Template'"}
            else:
                return {"status": "error", "message": "please provide part number in []"}
        else:
            return {"status": "error", "message": "Please provide 'Access Token' for this User %s"%res_user_obj.name}
        
    # Create Logic   
    @http.route('/api/product_create/', type='json', auth="public")
    def producte_create(self, **kw):
        access_token = kw.get("access_token")
        res_user_obj = request.env['res.users'].sudo().search([('id','=',request.env.context['uid'])])
        acs_token_ids = self.get_access_token(res_user_obj)
        if access_token in acs_token_ids:
            if kw.get("pp"):
                for i in kw.get("pp"):
                    part = i.get('part')
                    default_code = i.get('default_code')
                    revision = i.get('revision')
                    name = i.get('name')
                    part_type = i.get('part_type')
                    material = i.get('material')
                    length = i.get('length')
                    breadth = i.get('breadth')
                    height = i.get('height')
                    weight = i.get('weight')
                    lifecycle_status = i.get('lifecycle_status')
    
                    p_search_obj = request.env['product.template'].sudo().search([('default_code','=',default_code)])
#                     product_Categ_id = request.env['product.category'].sudo().search([('name','=','All')],limit=1)
                    if not p_search_obj:
                        sd = request.env['product.template'].sudo().create({
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
                            "company_id":request.env.company.id
    
                        })
                        print(sd)
    #                     status = 'Product Created Successfully'
#                     else:
#                         status = 'Product Name already Exists'
            return {"status": 'Product Created'}
        else:
            return {"status": "error", "message": "Please provide 'Access Token' for this User %s"%res_user_obj.name}

        # Product Update Logic
    @http.route('/api/product_update', type='json', auth="public")
    def producte_update(self, **kw):
            access_token = kw.get("access_token")
            res_user_obj = request.env['res.users'].sudo().search([('id', '=', request.env.context['uid'])])
            acs_token_ids = self.get_access_token(res_user_obj)
            if access_token in acs_token_ids:
                if kw.get("pp"):
                    for i in kw.get("pp"):
                        part = i.get('part')
                        default_code = i.get('default_code')
                        revision = i.get('revision')
                        name = i.get('name')
                        part_type = i.get('part_type')
                        material = i.get('material')
                        length = i.get('length')
                        breadth = i.get('breadth')
                        height = i.get('height')
                        weight = i.get('weight')
                        lifecycle_status = i.get('lifecycle_status')

                        p_search_obj = request.env['product.template'].sudo().search(
                            [('default_code', '=', default_code)])
                        if p_search_obj:
                            p_search_obj.write({
                                "part": part,
                                "default_code": default_code,
                                "revision": revision,
                                "name": name,
                                "part_type": part_type,
                                "material": material,
                                "length": length,
                                "breadth": breadth,
                                "height": height,
                                "weight": weight,
                                "lifecycle_status": lifecycle_status,
                                "company_id": request.env.company.id

                            })
                    return {"status": 'Product %s Updated ' % p_search_obj.id}
            else:
                return {"status": "error",
                        "message": "Please provide 'Access Token' for this User %s" % res_user_obj.name}

    @http.route('/api/token', type='json', auth="public")
    def get_api_token(self, **kw):   
        """The token URL to be used for getting the access_token:

        Args:
            **post must contain login and password.
        Returns:

            returns https response code 404 if failed error message in the body in json format
            and status code 202 if successful with the access_token.
        Example:
           import requests

           headers = {'content-type': 'text/plain', 'charset':'utf-8'}

           data = {
               'login': 'admin',
               'password': 'admin',
               'db': 'galago.ng'
            }
           base_url = 'http://odoo.ng'
           eq = requests.post(
               '{}/api/auth/token'.format(base_url), data=data, headers=headers)
           content = json.loads(req.content.decode('utf-8'))
           headers.update(access-token=content.get('access_token'))
        """
        _token = request.env["api.access_token"]
#         params = ["db", "login", "password"]
        db = kw.get('db')
        username=kw.get('login')
        password = kw.get('password')
#         params = {key: post.get(key) for key in params if post.get(key)}
#         db, username, password = (
#             params.get("db"),
#             post.get("login"),
#             post.get("password"),
#         )
          
        _credentials_includes_in_body = all([db, username, password])
        if not _credentials_includes_in_body:
            # The request post body is empty the credetials maybe passed via the headers.
            headers = request.httprequest.headers
            db = headers.get("db")
            username = headers.get("login")
            password = headers.get("password")
            _credentials_includes_in_headers = all([db, username, password])
            if not _credentials_includes_in_headers:
                # Empty 'db' or 'username' or 'password:
                return invalid_response(
                    "missing error", "either of the following are missing [db, username,password]", 403,
                )
        # Login in odoo database:
        try:
            request.session.authenticate(db, username, password)
        except AccessError as aee:
            return invalid_response("Access error", "Error: %s" % aee.name)
        except AccessDenied as ade:
            return invalid_response("Access denied", "Login, password or db invalid")
        except Exception as e:
            # Invalid database:
            info = "The database name is not valid {}".format((e))
            error = "invalid_database"
            _logger.error(info)
            return invalid_response("wrong database name", error, 403)

        uid = request.session.uid
        # odoo login failed:
        if not uid:
            info = "authentication failed"
            error = "authentication failed"
            _logger.error(info)
            return invalid_response(401, error, info)

        # Generate tokens
        access_token = _token.find_one_or_create_token(user_id=uid, create=True)
        request_value = []
        request_value.append({
            "uid": uid,
            "user_context": request.session.get_context() if uid else {},
            "company_id": request.env.user.company_id.id if uid else None,
            "company_ids": request.env.user.company_ids.ids if uid else None,
            "partner_id": request.env.user.partner_id.id,
            "access_token": access_token,
#             "expires_in": self._expires_in,
        })
        
        
        request.params['request_value'] = request_value
        print(request.params)
        return request.params
        # Successful response:
#         return request.Response(
#             status=200,
#             content_type="application/json; charset=utf-8",
#             headers=[("Cache-Control", "no-store"), ("Pragma", "no-cache")],
#             response=json.dumps(
#                 {
#                     "uid": uid,
#                     "user_context": request.session.get_context() if uid else {},
#                     "company_id": request.env.user.company_id.id if uid else None,
#                     "company_ids": request.env.user.company_ids.ids if uid else None,
#                     "partner_id": request.env.user.partner_id.id,
#                     "access_token": access_token,
#                     "expires_in": self._expires_in,
#                 }
#             ),
#         )