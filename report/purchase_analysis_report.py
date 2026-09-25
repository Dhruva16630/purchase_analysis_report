from odoo import models,fields,tools

class PurchaseAnalysisReport(models.Model):
    _name = "purchase.analysis.report"
    _description = "Purchase Analysis report"
    _auto = False
    
    # fields are grouped in according to tables names
    
    # purchase.order.line
    qty_ordered = fields.Float(
        string="Ordered Quantity",
        readonly = True
    )
    
    qty_received = fields.Float(
        string="Received Quantity",
        readonly = True
    )
    
    qty_billed = fields.Float(
        string="Billed Quantity",
        readonly = True
    )
    
    unit_price = fields.Float(
        string="Unit Price",
        readonly = True
    )
    
    total_amount = fields.Float(
        string="Amount",
        readonly = True
    )
    
    # purchase.order
    vender = fields.Many2one(
        "res.partner",
        string="Vender",
        readonly = True
    )
    
    purchase_order = fields.Char(
        string="Purchase Order",
        readonly = True
    )
    
    buyer = fields.Many2one(
        "res.users",
        string="Buyer",
        readonly = True
    )
    
    ordered_date = fields.Datetime(
        string="Order Date",
        readonly = True
    )
    
    expected_arrival = fields.Datetime(
        string="Expected Arrival",
        readonly = True
    )
    
    state = fields.Selection(
        selection=[
            ('draft', 'RFQ'),
            ('sent', 'RFQ Sent'),
            ('to approve', 'To Approve'),
            ('purchase', 'Purchase Order'),
            ('cancel', 'Cancelled')
        ]
    )
    
    # product.product
    product = fields.Many2one(
        "product.product",
        string="Product",
        readonly = True
    )
    
    # product.category
    product_category = fields.Many2one(
        "product.category",
        string="Product Category",
        readonly = True
    )
    
    
    def init(self):
        tools.drop_view_if_exists(
            self.env.cr,
            self._table
        )
        
        self.env.cr.execute("""
            CREATE VIEW purchase_analysis_report AS(
                SELECT
                    pol.id AS id,
                    pol.product_qty AS qty_ordered,
                    pol.qty_received AS qty_received,
                    pol.qty_invoiced AS qty_billed,
                    pol.price_unit AS unit_price,
                    pol.price_subtotal AS total_amount,
                    
                    po.partner_id AS vender,
                    po.name AS purchase_order,
                    po.user_id AS buyer,
                    po.date_approve AS ordered_date,
                    po.date_planned AS expected_arrival,
                    po.state AS state,
                    
                    pol.product_id AS product,
                    
                    pt.categ_id AS product_category
                    
                FROM purchase_order_line pol
                
                JOIN purchase_order po
                    ON po.id = pol.order_id
                
                JOIN product_product pp
                    ON pp.id = pol.product_id
                
                JOIN product_template pt
                    ON pt.id = pp.product_tmpl_id
                
                WHERE po.state = 'purchase'
            )
        """)