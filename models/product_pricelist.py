# -*- coding: utf-8 -*-

from odoo import fields,models,api,_
from odoo.exceptions import ValidationError
import re


class DynamicPricelistPrice(models.Model):
    _inherit = 'product.pricelist'

    enable_pricelist = fields.Boolean("Enable this Pricelist in Product List view")
    ir_ui_view_ref = fields.Many2one('ir.ui.view','Ir Ui View model saved Ref')  
    dynamic_pricelist_name = fields.Char()
    archived_enable_pricelist = fields.Boolean("Dynamic Pricelist Archived",default=False)
    
    enable_pricelist_variant = fields.Boolean("Enable this Pricelist in Product Variant List view")
    ir_ui_view_ref_variant = fields.Many2one('ir.ui.view','Ir Ui View model saved Ref for Variants')  
    archived_enable_pricelist_variant = fields.Boolean("Dynamic Pricelist Variant Archived",default=False)
    dynamic_pricelist_name_variant = fields.Char()
#     enable_pricelist_options = fields.Selection([('product', 'Product List View'),('product_variant', 'Product Variant List View')], string='Enable Pricelist In')
# 
#     
#     @api.onchange('enable_pricelist_options')
#     def onchange_pricelist_options(self):
#         if self.enable_pricelist_options == 'product':
#             self.enable_pricelist = True
#             self.enable_pricelist_variant = False
#         if self.enable_pricelist_options == 'product_variant':
#             self.enable_pricelist = False
#             self.enable_pricelist_variant = True

#     @api.onchange('enable_pricelist','enable_pricelist_variant')
#     def onchange_enable_pricelists_options(self):
#         if self.enable_pricelist == True:
#             self.enable_pricelist_variant = 
#         if self.enable_pricelist_variant == True:
#             self.enable_pricelist = False
# 
# #         if self.enable_pricelist == False:
# #             self.enable_pricelist = False
# #             self.env.cr.commit()
# # 
# #         if self.enable_pricelist_variant == False:
# #             self.env.cr.commit()
            

    @api.constrains('name')
    def _check_pricelist_name(self):
        # to validate pricelist name should not contain any whitespaces

        for record in self:
            price_list_ids = self.env['product.pricelist'].search([('name','=',record.name.strip()), ('id','!=', self.id)])
            if price_list_ids:
                raise ValidationError("Dear User! Pricelist name should be unique!")
            regex = re.compile('[@ !#$%^&*()<>?/\|}{~:]')
            if not (regex.search(record.name.strip()) == None):
                raise ValidationError("Dear User! Pricelist name should not contain white space or any other special character except Underscore(_)")
 

    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        # To change name while duplcating pricelist
        self.ensure_one()
        if default is None:
            default = {}
        if 'name' not in default:
            default['name'] = _("%s_copy", self.name)
        return super(DynamicPricelistPrice, self).copy(default=default)


    @api.model
    def create(self, vals):
        res = super(DynamicPricelistPrice, self).create(vals)
#         if vals.get('enable_pricelist'):
        if vals.get('enable_pricelist'):
            res.dynamic_pricelist_name = "x_"+vals.get('name')
            res.create_pricelist_dynamic_fields(vals)
        if vals.get('enable_pricelist_variant'):
            res.dynamic_pricelist_name_variant = "x__"+vals.get('name')
            res.create_pricelist_dynamic_fields(vals)
            
        return res

    

#     def write(self, vals):
# 
#         # below code to handle for archived scenario---------------start
#         if 'active' in vals:
#             if vals['active'] == False:
#                 if self.enable_pricelist == True:
#                     vals.update({'enable_pricelist':False,'archived_enable_pricelist':True})
#                 else:
#                     vals.update({'archived_enable_pricelist':False})
#                 
#                 if self.dynamic_pricelist_name:
#                     self.ir_ui_view_ref.write({
#                         'active' : False
#                     })
# 
#             if self.archived_enable_pricelist == True and vals['active'] == True:
#                 vals.update({'enable_pricelist':True,'archived_enable_pricelist':False})
#                 if self.dynamic_pricelist_name:
#                     try:
#                         self.ir_ui_view_ref.write({
#                             'active' : True
#                         })
#                     except:
#                         pass
#                 
#         # below code to handle for archived scenario---------------end
# 
#         res = super(DynamicPricelistPrice, self).write(vals)
# 
#         if 'enable_pricelist' in vals and 'archived_enable_pricelist' not in vals:
#             enable_pricelist = vals.get('enable_pricelist')            
#             if enable_pricelist:
#                 self.create_pricelist_dynamic_fields(vals)
#             else:         
#                 if self.dynamic_pricelist_name:
#                     self.ir_ui_view_ref.write({
#                         'active' : False
#                     })
#                     domain = []
#                     find_template = self.env['product.template'].search(domain)
#                     for data in find_template:                        
#                         data.write({
#                             '%s' %(self.dynamic_pricelist_name) : False
#                         })
#                     domain = []
#                     find_product = self.env['product.product'].search(domain)
#                     for data in find_product:                        
#                         data.write({
#                             '%s' %(self.dynamic_pricelist_name) : False
#                         })
#                     domain = [('name', '=', self.dynamic_pricelist_name)]
#                     find_fields = self.env['ir.model.fields'].search(domain)
#                     if find_fields:   
#                         for i in find_fields:
#                             if i.state == 'manual':                   
#                                 i.unlink()
#             self.dynamic_pricelist_name = "x_"+self.name
#         return res




    def write(self, vals):

        # below code to handle for company change scenario---------------start
        if 'company_id' in vals:
            if self.enable_pricelist:
                self.enable_pricelist = False
                self.env.cr.commit()
                vals['enable_pricelist'] = True
            if self.enable_pricelist_variant:
                self.enable_pricelist_variant = False
                self.env.cr.commit()
                vals['enable_pricelist_variant'] = True
        # below code to handle for company change scenario---------------end

        # below code to handle for archived scenario---------------start
        if 'active' in vals:
            if vals['active'] == False:
                if self.enable_pricelist == True:
                    vals.update({'enable_pricelist':False,'archived_enable_pricelist':True})
                else:
                    vals.update({'archived_enable_pricelist':False})
                
                if self.enable_pricelist_variant == True:
                    vals.update({'enable_pricelist_variant':False,'archived_enable_pricelist_variant':True})
                else:
                    vals.update({'archived_enable_pricelist_variant':False})
                
                if self.dynamic_pricelist_name and self.ir_ui_view_ref:
                    self.ir_ui_view_ref.write({
                        'active' : False
                    })
                
                if self.dynamic_pricelist_name_variant and self.ir_ui_view_ref_variant:
                    self.ir_ui_view_ref_variant.write({
                        'active' : False
                    })

            if self.archived_enable_pricelist == True and vals['active'] == True:
                vals.update({'enable_pricelist':True,'archived_enable_pricelist':False})
                if self.dynamic_pricelist_name and self.ir_ui_view_ref:
                    try:
                        self.ir_ui_view_ref.write({
                            'active' : True
                        })
                    except:
                        pass


            if self.archived_enable_pricelist_variant == True and vals['active'] == True:
                vals.update({'enable_pricelist_variant':True,'archived_enable_pricelist_variant':False})
                if self.dynamic_pricelist_name_variant and self.ir_ui_view_ref_variant:
                    try:
                        self.ir_ui_view_ref_variant.write({
                            'active' : True
                        })
                    except:
                        pass

        # below code to handle for archived scenario---------------end

        res = super(DynamicPricelistPrice, self).write(vals)

        if 'enable_pricelist' in vals and 'archived_enable_pricelist' not in vals:
            enable_pricelist = vals.get('enable_pricelist')            
            if enable_pricelist:
                if self.enable_pricelist_variant == True:
                    self.enable_pricelist_variant = False
                self.create_pricelist_dynamic_fields(vals)
            else:         
                if self.dynamic_pricelist_name:
                    self.ir_ui_view_ref.write({
                        'active' : False
                    })
                    domain = []
#                     find_template = self.env['product.template'].search(domain)
# #                     for data in find_template:                        
#                     for data in self.item_ids:                      
#                         if data.applied_on == '1_product':
#                             data.product_tmpl_id.write({
#                             '%s' %(self.dynamic_pricelist_name) : False
#                         })
                    domain = [('name', '=', self.dynamic_pricelist_name),('model','=','product.template')]
                    find_fields = self.env['ir.model.fields'].search(domain)
                    if find_fields:   
                        for i in find_fields:
                            if i.state == 'manual':                   
                                i.unlink()
            self.dynamic_pricelist_name = "x_"+self.name

        if 'enable_pricelist_variant' in vals and 'archived_enable_pricelist_variant' not in vals:
            enable_pricelist_variant = vals.get('enable_pricelist_variant')            
            if enable_pricelist_variant:
                if self.enable_pricelist == True:
                    self.enable_pricelist = False
                self.create_pricelist_dynamic_fields(vals)
            else:   
                if self.dynamic_pricelist_name_variant:
                    self.ir_ui_view_ref_variant.write({
                        'active' : False
                    })
                    domain = []
#                     find_product = self.env['product.product'].search(domain)
# #                     for data in find_product:                        
#                     for data in self.item_ids:
#                         if data.applied_on == '0_product_variant':
#                             data.product_id.write({
#                                 '%s' %(self.dynamic_pricelist_name_variant) : False
#                             })
                    domain = [('name', '=', self.dynamic_pricelist_name_variant),('model','=','product.product')]
                    find_fields = self.env['ir.model.fields'].search(domain)
                    if find_fields:   
                        for i in find_fields:
                            if i.state == 'manual':             
                                i.unlink()
            self.dynamic_pricelist_name_variant = "x__"+self.name
            
        if 'name' in vals:
            #pdb.set_trace()
            self.create_pricelist_dynamic_fields(vals)

        return res
    

    def unlink(self):
        if self:
            for res in self:
                if res.enable_pricelist:                    
                    res.ir_ui_view_ref.write({
                        'active' : False
                    })
                    domain = []
                    find_template = self.env['product.template'].search(domain)
#                     for data in find_template:   
                    for data in self.item_ids:                      
                        if data.applied_on == '1_product':
                            data.product_tmpl_id.write({
                                '%s' %(res.dynamic_pricelist_name) : False
                            })
#                     domain = []
#                     find_product = self.env['product.product'].search(domain)
#                     for data in find_product:                        
#                         data.write({
#                             '%s' %(res.dynamic_pricelist_name_variant) : False
#                         })
                    domain = [('name', '=', res.dynamic_pricelist_name)]
                    find_fields = self.env['ir.model.fields'].search(domain)
                    if find_fields:
                        for i in find_fields:
                            if i.state == 'manual':
                                i.unlink()

                if res.enable_pricelist_variant:                    
                    res.ir_ui_view_ref_variant.write({
                        'active' : False
                    })
#                     domain = []
#                     find_template = self.env['product.template'].search(domain)
#                     for data in find_template:                        
#                         data.write({
#                             '%s' %(res.dynamic_pricelist_name) : False
#                         })
                    domain = []
                    find_product = self.env['product.product'].search(domain)
#                     for data in find_product:      
                    for data in self.item_ids:
                        if data.applied_on == '0_product_variant':                  
                            data.product_id.write({
                                '%s' %(res.dynamic_pricelist_name_variant) : False
                            })
                    domain = [('name', '=', res.dynamic_pricelist_name_variant)]
                    find_fields = self.env['ir.model.fields'].search(domain)
                    if find_fields:
                        for i in find_fields:
                            if i.state == 'manual':
                                i.unlink()

        
        res = super(DynamicPricelistPrice, self).unlink()
        return res
    
    


    def create_pricelist_dynamic_fields(self,vals):
        enable_pricelist = ''
        enable_pricelist_variant = ''
        updated_name = ''
        if 'enable_pricelist' in vals:
            enable_pricelist = vals.get('enable_pricelist')
        if 'enable_pricelist_variant' in vals:
            enable_pricelist_variant = vals.get('enable_pricelist_variant')
        
        if 'name' in vals:
            updated_name = vals.get('name')
        #pdb.set_trace()
        if enable_pricelist or enable_pricelist_variant or updated_name:
#             if not fields_rec_ref:
#                 self.env['ir.model.fields'].create(pricee_vals)

            if enable_pricelist:

                model_id = self.env['ir.model'].sudo().search([('model', '=', 'product.template')])
                if vals.get('name'):
                    namee = vals.get('name')
                elif self.name:
                    namee = self.name
                price_vals = {
                    'field_description' : namee, 
                    'name' : "x_"+namee,
                    'model' : 'product.template',
                    'model_id' : model_id.id,
                    'ttype' : 'char',
                    'state' : 'manual'
                }          
                group_str = "product_variant_dynamic_pricelist_price.product_variant_dynamic_pricelist_price_manager"
                field_tech_name = price_vals['name']  
                field_name = "x_"+namee  

                fields_template_rec_ref = self.env['ir.model.fields'].sudo().search([('name','=',field_name),('model','=','product.template'),('model_id' ,'=', model_id.id), ('ttype' ,'=', 'char')])
                if not fields_template_rec_ref:
                    self.env['ir.model.fields'].create(price_vals)
    
#                 arch_base = _('<?xml version="1.0"?>'
#                             '<data>'
#                             '<field name="%s" position="%s">'
#                             '<field name="%s" groups="%s"/>'
#                             '</field>'
#                             '</data>') % ('list_price','after',field_tech_name,group_str)

                attrs = {'invisible':[('company_id_current','!=',self.env.company.id)]}
                if self.company_id:
                    arch_base = _('<?xml version="1.0"?>'
                                '<data>'
                                '<field name="%s" position="%s">'
                                '<field name="%s" groups="%s" attrs="%s" optional="show"/>'
                                '</field>'
                                '</data>') % ('list_price','after',field_tech_name,group_str,attrs)
                else:
                    arch_base = _('<?xml version="1.0"?>'
                            '<data>'
                            '<field name="%s" position="%s">'
                            '<field name="%s" groups="%s"/>'
                            '</field>'
                            '</data>') % ('list_price','after',field_tech_name,group_str)

                inherit_id = self.env.ref('product.product_template_tree_view')
    
                ir_view_obj = self.env['ir.ui.view'].create({'name': 'product.template.dynamic.pricelist.fields',
                                            'type': 'tree',
                                            'model': 'product.template',                                              
                                            'mode': 'extension',
                                            'inherit_id': inherit_id.id,
                                            'arch_base': arch_base,
                                            'active': True})
                self.ir_ui_view_ref = ir_view_obj.id
                
            if enable_pricelist_variant:
                
                model_id = self.env['ir.model'].sudo().search([('model', '=', 'product.product')])
                if vals.get('name'):
                    namee = vals.get('name')
                elif self.name:
                    namee = self.name
                pricee_vals = {
                    'field_description' : namee, 
                    'name' : "x__"+namee,
                    'model' : 'product.product',
                    'model_id' : model_id.id,
                    'ttype' : 'char',
                    'state' : 'manual'
                }          
                group_str = "product_variant_dynamic_pricelist_price.product_variant_dynamic_pricelist_price_manager" 
                field_tech_name_variant = pricee_vals['name']
                field_name = "x__"+namee  
                fields_rec_ref = self.env['ir.model.fields'].sudo().search([('name','=',field_name),('model','=','product.product'),('model_id' ,'=', model_id.id), ('ttype' ,'=', 'char')])

                model_id = self.env['ir.model'].sudo().search([('model', '=', 'product.product')])
                fields_product_variant_rec_ref = self.env['ir.model.fields'].sudo().search([('name','=',field_name),('model','=','product.product'),('model_id' ,'=', model_id.id), ('ttype' ,'=', 'char')])
                if not fields_product_variant_rec_ref:
                    self.env['ir.model.fields'].create(pricee_vals)
                
                
                attrs = {'invisible':[('company_id_current','!=',self.env.company.id)]}
                if self.company_id:
                    arch_base_variant = _('<?xml version="1.0"?>'
                                '<data>'
                                '<field name="%s" position="%s">'
                                '<field name="%s" groups="%s" attrs="%s" optional="show"/>'
                                '</field>'
                                '</data>') % ('lst_price','after',field_tech_name_variant,group_str,attrs)
                else:
                    arch_base_variant = _('<?xml version="1.0"?>'
                            '<data>'
                            '<field name="%s" position="%s">'
                            '<field name="%s" groups="%s"/>'
                            '</field>'
                            '</data>') % ('lst_price','after',field_tech_name_variant,group_str)
                variant_inherit_id = self.env.ref('product.product_product_tree_view')
    
                ir_view_obj_variant = self.env['ir.ui.view'].create({'name': 'product.product.dynamic.pricelist.fields',
                                            'type': 'tree',
                                            'model': 'product.product',                                              
                                            'mode': 'extension',
                                            'inherit_id': variant_inherit_id.id,
                                            'arch_base': arch_base_variant,
                                            'active': True})
                self.ir_ui_view_ref_variant = ir_view_obj_variant.id



            # additional code to handle the edit pricelist name
            
            if self.enable_pricelist == True and updated_name:

                model_id = self.env['ir.model'].sudo().search([('model', '=', 'product.template')])
                if vals.get('name'):
                    namee = vals.get('name')
                elif self.name:
                    namee = self.name
                price_vals = {
                    'field_description' : namee, 
                    'name' : "x_"+namee,
                    'model' : 'product.template',
                    'model_id' : model_id.id,
                    'ttype' : 'char',
                    'state' : 'manual'
                }          
                group_str = "product_variant_dynamic_pricelist_price.product_variant_dynamic_pricelist_price_manager"
                field_tech_name = price_vals['name']  
                field_name = "x_"+namee  
                if self.dynamic_pricelist_name:
                    field_name = self.dynamic_pricelist_name

                fields_template_rec_ref = self.env['ir.model.fields'].sudo().search([('name','=',field_name),('model','=','product.template'),('model_id' ,'=', model_id.id), ('ttype' ,'=', 'char')])
                if not fields_template_rec_ref:
                    self.env['ir.model.fields'].create(price_vals)
    
#                 arch_base = _('<?xml version="1.0"?>'
#                             '<data>'
#                             '<field name="%s" position="%s">'
#                             '<field name="%s" groups="%s"/>'
#                             '</field>'
#                             '</data>') % ('list_price','after',field_tech_name,group_str)

                attrs = {'invisible':[('company_id_current','!=',self.env.company.id)]}
                if self.company_id:
                    arch_base = _('<?xml version="1.0"?>'
                                '<data>'
                                '<field name="%s" position="%s">'
                                '<field name="%s" groups="%s" attrs="%s" optional="show" string="%s"/>'
                                '</field>'
                                '</data>') % ('list_price','after',field_name,group_str,attrs,namee)
                else:
                    arch_base = _('<?xml version="1.0"?>'
                            '<data>'
                            '<field name="%s" position="%s">'
                            '<field name="%s" groups="%s" string="%s"/>'
                            '</field>'
                            '</data>') % ('list_price','after',field_name,group_str,namee)

                inherit_id = self.env.ref('product.product_template_tree_view')
    
                if self.ir_ui_view_ref:
                    self.ir_ui_view_ref.write({
                                            'arch_base': arch_base
                                               })
                else:
                    ir_view_obj = self.env['ir.ui.view'].create({'name': 'product.template.dynamic.pricelist.fields',
                                                'type': 'tree',
                                                'model': 'product.template',                                              
                                                'mode': 'extension',
                                                'inherit_id': inherit_id.id,
                                                'arch_base': arch_base,
                                                'active': True})
                    self.ir_ui_view_ref = ir_view_obj.id
            



            if self.enable_pricelist_variant == True and updated_name:
                
                model_id = self.env['ir.model'].sudo().search([('model', '=', 'product.product')])
                if vals.get('name'):
                    namee = vals.get('name')
                elif self.name:
                    namee = self.name
                pricee_vals = {
                    'field_description' : namee, 
                    'name' : "x__"+namee,
                    'model' : 'product.product',
                    'model_id' : model_id.id,
                    'ttype' : 'char',
                    'state' : 'manual'
                }          
                group_str = "product_variant_dynamic_pricelist_price.product_variant_dynamic_pricelist_price_manager" 
                field_tech_name_variant = pricee_vals['name']
                field_name = "x__"+namee  
                if self.dynamic_pricelist_name_variant:
                    field_name = self.dynamic_pricelist_name_variant
                fields_rec_ref = self.env['ir.model.fields'].sudo().search([('name','=',field_name),('model','=','product.product'),('model_id' ,'=', model_id.id), ('ttype' ,'=', 'char')])

                model_id = self.env['ir.model'].sudo().search([('model', '=', 'product.product')])
                fields_product_variant_rec_ref = self.env['ir.model.fields'].sudo().search([('name','=',field_name),('model','=','product.product'),('model_id' ,'=', model_id.id), ('ttype' ,'=', 'char')])
                if not fields_product_variant_rec_ref:
                    self.env['ir.model.fields'].create(pricee_vals)
                
                attrs = {'invisible':[('company_id_current','!=',self.env.company.id)]}
                if self.company_id:
                    arch_base_variant = _('<?xml version="1.0"?>'
                                '<data>'
                                '<field name="%s" position="%s">'
                                '<field name="%s" groups="%s" attrs="%s" optional="show" string="%s"/>'
                                '</field>'
                                '</data>') % ('lst_price','after',field_name,group_str,attrs,namee)
                else:
                    arch_base_variant = _('<?xml version="1.0"?>'
                            '<data>'
                            '<field name="%s" position="%s">'
                            '<field name="%s" groups="%s" string="%s"/>'
                            '</field>'
                            '</data>') % ('lst_price','after',field_name,group_str,namee)
                variant_inherit_id = self.env.ref('product.product_product_tree_view')
    
    
                if self.ir_ui_view_ref_variant:
                    self.ir_ui_view_ref_variant.write({
                                            'arch_base': arch_base_variant
                                               })

                
                else:
                    ir_view_obj_variant = self.env['ir.ui.view'].create({'name': 'product.product.dynamic.pricelist.fields',
                                            'type': 'tree',
                                            'model': 'product.product',                                              
                                            'mode': 'extension',
                                            'inherit_id': variant_inherit_id.id,
                                            'arch_base': arch_base_variant,
                                            'active': True})
                    self.ir_ui_view_ref_variant = ir_view_obj_variant.id



            
            

    
