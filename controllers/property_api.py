#
##
import json
from urllib.parse import parse_qs

import math
from odoo import http
from odoo.http import request
def invalid_response(error, status):
    response_body = {
        'error': error
    }
    return request.make_json_response(response_body, status=status)




def valid_response(data,status,pagination_info):
    response_data = {
        'data':data,
          'message': "successful"

    }
    if pagination_info:
        response_data['pagination_info'] = pagination_info

    return request.make_json_response(response_data, status=status)




class PropertyApi(http.Controller):
    @http.route("/v1/property/",methods=["POST"], type="http", auth="none", csrf=False)
    def post_property(self):
        args = request.httprequest.data.decode()
        vals = json.loads(args)
        # print(vals)
        if not vals.get('name'):
            return request.make_json_response({
                    "message":"Name is Required ",
            },status = 400)

        try:
            res = request.env['property'].sudo().create(vals)
            # print(res)


            if res:
                return request.make_json_response({
                    "message":"Property has been created successfuly",
                    "id": res.id,
                    "name": res.name,
                    "postcode": res.postcode,

                }, status = 201)
        except Exception as error:
            return request.make_json_response({
                "message": "error",

            }, status=400)


    @http.route("/v1/property/json", methods=["POST"], type="json", auth="none", csrf=False)
    def post_property_json(self):
        args = request.httprequest.data.decode()
        vals = json.loads(args)
        # print(vals)
        res = request.env['property'].sudo().create(vals)
        print(res)
        if res:
            return [{
                "message": "Property has been created successfuly"

            }]

    # endpoint by update operation method [PUT]
    @http.route("/v1/property/<int:property_id>", methods=["PUT"], type="http", auth="none", csrf=False)

    def update_property(self,property_id):
        try:

            property_id = request.env['property'].sudo().search([('id','=', property_id)])
            if not property_id:
                return request.make_json_response({
                    "message": "ID does not exist!",
                }, status=400)

            args = request.httprequest.data.decode()
            vals = json.loads(args)
            # for update el value in ui
            property_id.write(vals)
            return request.make_json_response({
                "message": "Property has been updated successfuly",
                "id": property_id.id,
                "name": property_id.name,
                "postcode": property_id.postcode,

            },status=200)
        except Exception as error:
            return request.make_json_response({
                "message":error,
            }, status=400)


# # search or reaed operation
    @http.route("/v1/property/<int:property_id>", method=["GET"], type="http", auth="none", csrf=False)
    def get_property(self,property_id):
        try:
            property_id = request.env['property'].sudo().search([('id','=', property_id)])
            if not property_id:
                return invalid_response(
                    # invalid response
                 "There is no property match this id", status=400)
                 # VALID RESPONSE
            return valid_response({
                    # GET EL DATA
                "id": property_id.id,
                "name": property_id.name,
                "ref": property_id.ref,
                "postcode": property_id.postcode,
                "bedrooms": property_id.bedrooms,

            }, status=200)

        except Exception as error:
            return request.make_json_response({
                "error": error,
            }, status=400)



# delete operation

    @http.route("/v1/property/<int:property_id>", methods=["DELETE"], type="http", auth="none", csrf=False)
    def delete_property(self, property_id):
        try:
            property_id = request.env['property'].sudo().search([('id', '=', property_id)])
            if not property_id:
                return request.make_json_response({
                    "message":"ID does not exist!"

                },status=400)
            property_id.unlink()
            return request.make_json_response({
                "message": "Property has been deleted successfully"

            }, status=200)


        except Exception as error:
            return request.make_json_response({
                "error": error,
            }, status=400)





# GET All lists \\
    @http.route("/v1/properties", methods=["GET"], type="http", auth="none", csrf=False)
    def get_property_list(self):
        try:
            # to filter records by state sold
            params = parse_qs(request.httprequest.query_string.decode('utf-8'))
            property_domain =[]
            page = offset = None
            limit = 5
            if params:
                if params.get('limit'):
                    limit = int(params.get('limit')[0])
                if params.get('page'):
                    page = int(params.get('page')[0])
            # if params.get('limit'):
            #     print(params.get('limit'))
            # if params.get('page'):
            #     print(params.get('page'))

            if page:
                offset = (page *limit) - limit

            # usese params in filteration
            if params.get('state'):
                property_domain +=[('state','=',params.get('state')[0])]

            property_ids = request.env['property'].sudo().search(property_domain, offset=offset, limit=limit, order='id desc')
            property_count = request.env['property'].sudo().search_count(property_domain)
            # print(page)
            # print(limit)
            # print(offset)
            # print(property_ids)
            # print(property_count)
            if not property_ids:
                return  request.make_json_response({
                    "error":"There ara not records"
                },status=400)
            return valid_response([{
                # GET EL DATA
                "id": property_id.id,
                "name": property_id.name,
                "ref": property_id.ref,
                "postcode": property_id.postcode,
                "bedrooms": property_id.bedrooms,

            } for property_id in property_ids ],

                # to handle response with frontend by meta data
                pagination_info={
                    'page': page if page else 1,
                     'limit': limit,
                      'pages': math.ceil(property_count / limit) if limit else 1,
                    'count' : property_count

                }
                , status=200)



        except Exception as error:
            return request.make_json_response({
                "error": error,
            }, status=400)


