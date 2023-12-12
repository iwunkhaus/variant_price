# -*- coding: utf-8 -*-

from odoo import fields,models,api,_



class PricelistBooleanProduct(models.Model):
    _inherit = "product.template"

    enable_pricelist_boolean = fields.Boolean("Pricelist Boolean",compute="_load_allow_pricelist_boolean_field",default=False)
    product_pricelist_items = fields.One2many("product.pricelist.item","product_tmpl_id",string="Pricelist Items")
#     product_pricelist_item = fields.Many2many("product.pricelist.item","prod_pricelist_item_rel","prod_tmpl_id","pricelist_item_id",string="Pricelist Items")
    company_id_current = fields.Many2one('res.company', 'Current Company', compute='_get_company_id')

    
    def _get_company_id(self):
        self.company_id_current = self.env.company.id



    def _load_allow_pricelist_boolean_field(self):
        if self:            
            for rec in self:          
                rec.enable_pricelist_boolean = True                
                dicc =  rec.fields_get()
                list_values = [name for name in dicc.keys() if 'x_' in name]
                for data in list_values:
                    domain = [('dynamic_pricelist_name', '=', data)]
                   
                    find_pricelist = self.env['product.pricelist'].search(domain)
                    if find_pricelist:    
                                           
                        for item in find_pricelist.item_ids:   
                            if rec.id == item.product_tmpl_id.id and item.applied_on == '1_product':                                                                              
                                rec.with_context(test=True).write({
                                    '%s' %(data): item.price
                                })
                            

                
    def write(self,vals):
        res = super(PricelistBooleanProduct, self).write(vals)
        if self.env.context.get('test') != True:
            for rec in self:                
                for data,value in vals.items():
                    if 'x_' in data:
                        domain = [('dynamic_pricelist_name', '=', data)]
                        find_pricelist = self.env['product.pricelist'].search(domain)      
                        
                        curr_model = 'product.template'
                        if 'params' in self.env.context:
                            if 'model' in self.env.context['params']:
                                curr_model = self.env.context['params']['model']
                        
                        if curr_model == 'product.pricelist' and vals[data] == False:
                            break;
                        
                        if find_pricelist:
                            pricelist_products_list = find_pricelist.item_ids.mapped('product_tmpl_id') 
                            prod_not_exist = []
                            prod_not_exist_dict = {}
                            for item in find_pricelist.item_ids:                            
                                if rec.id == item.product_tmpl_id.id and item.applied_on == '1_product':
                                    if value:
                                        item.write({
                                            'fixed_price' : value.replace("$","").strip()
                                        })
                                    else:
                                        item.write({
                                            'fixed_price' : value
                                        })
                                    if rec.id in prod_not_exist :
                                        prod_not_exist.remove(rec.id)
                                        
                                
                                else:
                                    if rec.id not in prod_not_exist :
                                        prod_not_exist.append(rec.id) 
                                        prod_not_exist_dict.update({rec.id:[rec.id,value]})

                            if not find_pricelist.item_ids :
                                prod_not_exist_dict.update({rec.id:[rec.id,vals[data]]})
                                prod_not_exist.append(rec.id)
                            
                            if prod_not_exist:
                                for prod in prod_not_exist:
                                    if prod not in pricelist_products_list.ids:
                                        self.env['product.pricelist.item'].create({
                                                                           'product_tmpl_id': prod_not_exist_dict[rec.id][0],
                                                                           'pricelist_id':find_pricelist.id,
                                                                           'fixed_price':prod_not_exist_dict[rec.id][1],
                                                                           'applied_on':'1_product'
                                                                           })

                                    
        return res




class PricelistVariantBooleanProduct(models.Model):
    _inherit = "product.product"

    enable_pricelist_boolean = fields.Boolean("Pricelist Boolean",compute="_load_allow_pricelist_boolean_field",default=False)
    product_pricelist_items = fields.One2many("product.pricelist.item","product_id",string="Pricelist Items")
#     company_id_1 = fields.Many2one('res.company', 'Current Company', required=True, index=True, default=lambda self: self.env.company)
    company_id_current = fields.Many2one('res.company', 'Current Company', compute='_get_company_id')

    
    def _get_company_id(self):
        self.company_id_current = self.env.company.id
        
        
    def _load_allow_pricelist_boolean_field(self):
        if self:            
            for rec in self:          
                rec.enable_pricelist_boolean = True                
                dicc =  rec.fields_get()
                list_values = [name for name in dicc.keys() if 'x__' in name]
                for data in list_values:
                    domain = [('dynamic_pricelist_name_variant', '=', data)]
                   
                    find_pricelist = self.env['product.pricelist'].search(domain)
                    if find_pricelist:    
                                           
                        for item in find_pricelist.item_ids:                            
                            if rec.id == item.product_id.id and item.applied_on == '0_product_variant':                                                                                
                                rec.with_context(test=True).write({
                                    '%s' %(data): item.price
                                })
                                
                                
                
    def write(self,vals):
        res = super(PricelistVariantBooleanProduct, self).write(vals)
        if self.env.context.get('test') != True:
            for rec in self:                
                for data,value in vals.items():
                    if 'x__' in data:
                        domain = [('dynamic_pricelist_name_variant', '=', data)]
                        find_pricelist = self.env['product.pricelist'].search(domain)      
                        
                        curr_model = 'product.product'
                        if 'params' in self.env.context:
                            if 'model' in self.env.context['params']:
                                curr_model = self.env.context['params']['model']
                        
                        if curr_model == 'product.pricelist' and vals[data] == False:
                            break;
                        
                        if find_pricelist:
                            pricelist_products_list = find_pricelist.item_ids.mapped('product_id') 
                            prod_not_exist = []
                            prod_not_exist_dict = {}
                            for item in find_pricelist.item_ids:                            
                                if rec.id == item.product_id.id and item.applied_on == '0_product_variant':
                                    if value:
                                        item.write({
                                            'fixed_price' : value.replace("$","").strip()
                                        })
                                    else:
                                        item.write({
                                            'fixed_price' : value
                                        })

                                    if rec.id in prod_not_exist :
                                        prod_not_exist.remove(rec.id)
                                        
                                
                                else:
                                    if rec.id not in prod_not_exist :
                                        prod_not_exist.append(rec.id) 
                                        prod_not_exist_dict.update({rec.id:[rec.id,value]})
                            
                            if not find_pricelist.item_ids :
                                prod_not_exist_dict.update({rec.id:[rec.id,vals[data]]})
                                prod_not_exist.append(rec.id)
                            
                            if prod_not_exist:
                                for prod in prod_not_exist:
                                    if prod not in pricelist_products_list.ids:
                                        self.env['product.pricelist.item'].create({
                                                                           'product_id': prod_not_exist_dict[rec.id][0],
                                                                           'pricelist_id':find_pricelist.id,
                                                                           'fixed_price':prod_not_exist_dict[rec.id][1],
                                                                           'applied_on':'0_product_variant'
                                                                           })

                                    
        return res
    

 
class PricelistItem(models.Model):
    _inherit = "product.pricelist.item"
 
#     enable_pricelist = fields.Boolean(related="pricelist_id.enable_pricelist",string="Enable this Pricelist in Product List view",store=True)

#     allow_enable_pricelist = fields.Boolean(string="Enable this Pricelist in Product List view",default=False)
  
      
#     @api.depends('enable_pricelist','pricelist_id')
#     @api.onchange('enable_pricelist','pricelist_id')
#     def onchange_enable_pricelist(self):
#         for i in self:
#             if i.enable_pricelist == True:
#                 i.pricelist_id.enable_pricelist = True




#     @api.depends('allow_enable_pricelist')
#     @api.onchange('allow_enable_pricelist')
#     def onchange_enable_pricelist_boolean(self):
#         for i in self:
#             if i.allow_enable_pricelist == True:
#                 i.pricelist_id.enable_pricelist = True
#         
#     
#     @api.depends('pricelist_id')
#     @api.onchange('pricelist_id')
#     def onchange_enable_pricelist(self):
#         for i in self:
#             if i.pricelist_id:
#                 i.allow_enable_pricelist = i.pricelist_id.enable_pricelist
    
    

    
    
    




