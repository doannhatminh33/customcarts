import html
import math
from datetime import datetime

from cartmigration.models.basecart import LeBasecart
from cartmigration.libs.utils import *


class LeCartCustom(LeBasecart):
    def display_config_source(self):
        parent = super().display_config_source()
        if parent['result'] != 'success':
            return parent
        response = response_success()
        order_status_data = {
            'completed': 'Completed'
        }
        language_data = {
            1: "Default Language"
        }
        self._notice['src']['category_root'] = 1
        self._notice['src']['site'] = {
            1: 'Default Shop'
        }
        self._notice['src']['category_data'] = {
            1: 'Default Category',
        }
        self._notice['src']['support']['language_map'] = True
        self._notice['src']['support']['country_map'] = False
        self._notice['src']['support']['customer_group_map'] = False
        self._notice['src']['support']['taxes'] = True
        self._notice['src']['support']['manufacturers'] = False
        self._notice['src']['support']['reviews'] = False
        self._notice['src']['support']['add_new'] = True
        self._notice['src']['support']['skip_demo'] = False
        self._notice['src']['support']['customer_group_map'] = False
        self._notice['src']['languages'] = language_data
        self._notice['src']['order_status'] = order_status_data
        response['result'] = 'success'
        return response

    def display_config_target(self):
        return response_success()

    def display_import_source(self):
        if self._notice['config']['add_new']:
            recent = self.get_recent(self._migration_id)
            if recent:
                types = ['address_book', 'categories', 'categories_description', 'countries', 'currencies', 'customers',
                         'customers_info', 'languages', 'orders', 'orders_products', 'orders_total', 'products',
                         'products_description', 'products_to_categories', 'zones']
                for _type in types:
                    self._notice['process'][_type]['id_src'] = recent['process'][_type]['id_src']
                    self._notice['process'][_type]['total'] = 0
                    self._notice['process'][_type]['imported'] = 0
                    self._notice['process'][_type]['error'] = 0

        queries = {
            'categories': {
                'type': 'select',
                'query': "SELECT COUNT(1) AS count FROM categories WHERE categories_id > " + to_str(
                    self._notice['process']['categories']['id_src']),
            },
            'customers': {
                'type': 'select',
                'query': "SELECT COUNT(1) AS count FROM customers WHERE customers_id > " + to_str(
                    self._notice['process']['customers']['id_src']),
            },
            'orders': {
                'type': 'select',
                'query': "SELECT COUNT(1) AS count FROM orders WHERE orders_id > " + to_str(
                    self._notice['process']['orders']['id_src']),
            },
            'products': {
                'type': 'select',
                'query': "SELECT COUNT(1) AS count FROM products WHERE products_id > " + to_str(
                    self._notice['process']['products']['id_src']),
            }
        }
        count = self.get_connector_data(self.get_connector_url('query'), {
            'serialize': True,
            'query': json.dumps(queries)
        })
        if (not count) or (count['result'] != 'success'):
            return response_error()

        real_totals = dict()
        for key, row in count['data'].items():
            total = self.list_to_count_import(row, 'count')
            real_totals[key] = total
        for key, total in real_totals.items():
            self._notice['process'][key]['total'] = total
        return response_success()

    def display_import_target(self):
        return response_success()

    def display_confirm_source(self):
        return response_success()

    def display_confirm_target(self):
        self._notice['target']['clear']['function'] = 'clear_target_taxes'
        return response_success()

    # TODO: CLEAR

    def clear_target_address_book(self):
        next_clear = {
            'result': 'process',
            'function': 'clear_target_categories',
        }
        self._notice['target']['clear'] = next_clear
        return next_clear

    def clear_target_categories(self):
        next_clear = {
            'result': 'process',
            'function': 'clear_target_categories_description',
        }
        self._notice['target']['clear'] = next_clear
        return next_clear

    def clear_target_categories_description(self):
        next_clear = {
            'result': 'process',
            'function': 'clear_target_countries',
        }
        self._notice['target']['clear'] = next_clear
        return next_clear

    def clear_target_countries(self):
        next_clear = {
            'result': 'process',
            'function': 'clear_target_currencies',
        }
        self._notice['target']['clear'] = next_clear
        return next_clear

    def clear_target_currencies(self):
        next_clear = {
            'result': 'process',
            'function': 'clear_target_customers',
        }
        self._notice['target']['clear'] = next_clear
        return next_clear

    def clear_target_customers(self):
        next_clear = {
            'result': 'process',
            'function': 'clear_target_customers_info',
        }
        self._notice['target']['clear'] = next_clear
        return next_clear

    def clear_target_customers_info(self):
        next_clear = {
            'result': 'process',
            'function': 'clear_target_languages',
        }
        self._notice['target']['clear'] = next_clear
        return next_clear

    def clear_target_laguages(self):
        next_clear = {
            'result': 'process',
            'function': 'clear_target_orders',
        }
        self._notice['target']['clear'] = next_clear
        return next_clear

    def clear_target_orders(self):
        next_clear = {
            'result': 'process',
            'function': 'clear_target_orders_products',
        }
        self._notice['target']['clear'] = next_clear
        return next_clear

    def clear_target_orders_products(self):
        next_clear = {
            'result': 'process',
            '	function': 'clear_target_orders_total',
        }
        self._notice['target']['clear'] = next_clear
        return next_clear

    def clear_target_orders_total(self):
        next_clear = {
            'result': 'process',
            'function': 'clear_target_products',
        }
        self._notice['target']['clear'] = next_clear
        return next_clear

    def clear_target_products(self):
        next_clear = {
            'result': 'process',
            'function': 'clear_target_products_description',
        }
        self._notice['target']['clear'] = next_clear
        return next_clear

    def clear_target_products_description(self):
        next_clear = {
            'result': 'process',
            'function': 'clear_target_products_to_categories',
        }
        self._notice['target']['clear'] = next_clear
        return next_clear

    def clear_target_products_to_categories(self):
        next_clear = {
            'result': 'process',
            'function': 'clear_target_zones',
        }
        self._notice['target']['clear'] = next_clear
        return next_clear

    # TODO: category

    def prepare_categories_import(self):
        return self

    def prepare_categories_export(self):
        return self

    def get_categories_main_export(self):
        id_src = self._notice['process']['categories']['id_src']
        limit = self._notice['setting']['categories']
        query = {
            'type': 'select',
            'query': "SELECT * FROM categories WHERE categories_id > " + to_str(
                id_src) + " ORDER BY categories_id ASC LIMIT " + to_str(limit)
        }
        categories = self.select_data_connector(query, 'categories')

        if not categories or categories['result'] != 'success':
            return response_error('could not get categories main to export')
        return categories

    def get_categories_ext_export(self, categories):
        url_query = self.get_connector_url('query')

        category_ids = duplicate_field_value_from_list(categories['data'], 'categories_id')

        categories_ext_queries = {
            'categories_description': {
                'type': 'select',
                'query': "SELECT * FROM categories_description WHERE categories_id IN " + self.list_to_in_condition(
                    category_ids)
            },
            'languages': {
                'type': 'select',
                'query': "SELECT * FROM languages as lg INNER JOIN categories_description as cd" + " ON lg.languages_id = cd.language_id WHERE cd.categories_id IN " + self.list_to_in_condition(
                    map(int, category_ids))
            },
        }
        categories_ext = self.select_multiple_data_connector(categories_ext_queries, 'categories')

        if not categories_ext or categories_ext['result'] != 'success':
            return response_warning()
        return categories_ext

    def convert_category_export(self, category, categories_ext):
        category_data = self.construct_category()
        parent = self.construct_category_parent()

        parent['id'] = 0
        if category['parent_id']:
            parent_data = self.get_category_parent(category['parent_id'])
            if parent_data['result'] == 'success' and parent_data['data']:
                parent = parent_data['data']
                code_parent = parent_data['url_key'] if 'url_key' in parent_data else ''

        category_data['id'] = category['categories_id']
        category_data['parent'] = parent

        category_description = \
        get_list_from_list_by_field(categories_ext['data']['categories_description'], 'categories_id',
                                    category['categories_id'])[0]
        category_data['name'] = category_description['categories_name']

        for language_id, label in self._notice['src']['languages'].items():
            category_language_data = self.construct_category_lang()
            lang = get_list_from_list_by_field(categories_ext['data']['languages'], 'languages_id', language_id)[0]
            category_language_data['name'] = lang['name']
            category_data['languages'][language_id] = category_language_data

        if category['categories_image']:
            category_data['thumb_image']['url'] = 'http://localhost/customcart/images/'
            category_data['thumb_image']['path'] = category['categories_image']

        category_data['sort_order'] = category['sort_order']
        category_data['created_at'] = to_str(datetime.fromtimestamp(to_int(category['date_added']))) if category[
            'date_added'] else '0000-00-00 00:00:00'
        category_data['updated_at'] = to_str(datetime.fromtimestamp(to_int(category['last_modified']))) if category[
            'last_modified'] else '0000-00-00 00:00:00'

        return response_success(category_data)

    def get_category_id_import(self, convert, category, categories_ext):
        return category['categories_id']

    def check_category_import(self, convert, category, categories_ext):
        id_imported = self.get_map_field_by_src(self.TYPE_CATEGORY, convert['id'], convert['code'])
        return id_imported

    def router_category_import(self, convert, category, categories_ext):
        return response_success('category_import')

    def before_category_import(self, convert, category, categories_ext):
        return response_success()

    def category_import(self, convert, category, categories_ext):
        return response_success(0)

    def after_category_import(self, category_id, convert, category, categories_ext):
        return response_success()

    def addition_category_import(self, convert, category, categories_ext):
        return response_success()

    # TODO: PRODUCT
    def prepare_products_import(self):
        return self

    def prepare_products_export(self):
        return self

    def get_products_main_export(self):
        id_src = self._notice['process']['products']['id_src']
        limit = 4
        query = {
            'type': 'select',
            'query': "SELECT * FROM products WHERE products_id > " + to_str(
                id_src) + " ORDER BY products_id ASC LIMIT " + to_str(limit)
        }

        products = self.get_connector_data(self.get_connector_url('query'), {'query': json.dumps(query)})
        if not products or products['result'] != 'success':
            return response_error()
        return products

    def get_products_ext_export(self, products):
        url_query = self.get_connector_url('query')
        product_ids = duplicate_field_value_from_list(products['data'], 'products_id')
        product_id_con = self.list_to_in_condition(product_ids)
        product_id_query = self.product_to_in_condition_seourl(product_ids)

        product_ext_queries = {
            'products_description': {
                'type': "select",
                'query': "SELECT * FROM products_description WHERE products_id IN " + product_id_con,
            },
            'products_to_categories': {
                'type': 'select',
                'query': "SELECT * FROM products_to_categories WHERE products_id IN " + product_id_con,
            },
        }

        product_ext = self.select_multiple_data_connector(product_ext_queries, "products")
        if (not product_ext) or product_ext['result'] != 'success':
            return response_error()

        product_ext = self.select_multiple_data_connector(product_ext_queries, "products")
        if (not product_ext) or product_ext['result'] != 'success':
            return response_error()

        product_ext_rel_queries = {
        }

        product_ext_rel = self.select_multiple_data_connector(product_ext_rel_queries, "products_description")
        if (not product_ext_rel) or (product_ext_rel['result'] != 'success'):
            return response_error()

        product_ext = self.sync_connector_object(product_ext, product_ext_rel)
        return product_ext

    def convert_product_export(self, product, products_ext):
        products_ext_data = products_ext['data']

        product_data = self.construct_product()
        product_data['id'] = product['products_id']
        product_data['sku'] = product['products_upc_code']
        product_data['price'] = product['products_msrp']
        product_data['special_price']['price'] = product['products_wholesale_price']
        product_data['weight'] = product['products_weight']
        product_data['length'] = to_decimal(product['products_length'])
        product_data['width'] = to_decimal(product['products_width'])
        product_data['height'] = to_decimal(product['products_height'])
        if to_int(product['products_status']) > 0:
            status = True
        else:
            status = False

        product_data['status'] = product['products_status']
        product_data['manage_stock'] = True
        product_data['qty'] = product['products_quantity']
        product_data['date_available'] = product['products_date_available']
        product_data['created_at'] = to_str(datetime.fromtimestamp(to_int(product['products_date_added']))) if product[
            'products_date_added'] else get_current_time()
        product_data['updated_at'] = to_str(
            datetime.fromtimestamp(to_int(product['products_last_modified']))) if to_int(
            product['products_last_modified']) else product_data['created_at']

        product_description = \
        get_list_from_list_by_field(products_ext_data['products_description'], 'products_id', product['products_id'])[0]

        product_data['name'] = product_description['products_name']
        product_data['description'] = html.unescape(product_description['products_description'])

        url_product_image = 'http://localhost/customcart/images/'
        check_thumbnail = False
        if product['products_image'] != '':
            check_thumbnail = True
            product_data['thumb_image']['url'] = url_product_image
            product_data['thumb_image']['path'] = product['products_image']

        product_categories = get_list_from_list_by_field(products_ext_data['products_to_categories'], 'products_id',
                                                         product['products_id'])
        if product_categories:
            for product_category in product_categories:
                product_category_data = self.construct_product_category()
                product_category_data['id'] = product_category['categories_id']
                product_data['categories'].append(product_category_data)

        if self._notice['config']['seo_301']:
            detect_seo = self.detect_seo()
            product_data['seo'] = getattr(self, 'products_' + detect_seo)(product, products_ext)
        return response_success(product_data)

    def get_product_id_import(self, convert, product, products_ext):
        return product['products_id']

    def check_product_id_import(self, convert, product, products_ext):
        return True if self.get_map_field_by_src(self.TYPE_PRODUCT, convert['products_id'], convert['code']) else False

    def router_product_id_import(self, convert, product, products_ext):
        return response_success('product_import')

    def before_product_import(self, convert, product, products_ext):
        return response_success()

    def product_import(self, convert, product, products_ext):
        return response_success(0)

    def after_product_import(self, product_id, convert, product, products_ext):
        return response_success()

    def addition_product_import(self, convert, product, products_ext):
        return response_success()

    # TODO: CUSTOMER

    def prepare_customers_import(self):
        query = {
            'type': 'query',
            'query': "ALTER TABLE customers MODIFY COLUMN customers_password varchar(255)"
        }
        self.import_data_connector(query, 'customer')
        return self

    def prepare_customers_export(self):
        return self

    def get_customers_main_export(self):
        id_src = self._notice['process']['customers']['id_src']
        limit = self._notice['setting']['customers']
        query = {
            'type': 'select',
            'query': "SELECT * FROM customers WHERE customers_id > " + to_str(
                id_src) + " ORDER BY customers_id ASC LIMIT " + to_str(limit)
        }

        customers = self.select_data_connector(query, "customers")
        if not customers or customers['result'] != 'success':
            return response_error('Could not get customers main to export')
        return customers

    def get_customers_ext_export(self, customers):
        customer_ids = duplicate_field_value_from_list(customers['data'], 'customers_id')
        customer_ext_queries = {
            'address_book': {
                'type': 'select',
                'query': "SELECT * FROM address_book WHERE customers_id IN " + self.list_to_in_condition(customer_ids)
            },
            'customers_info': {
                'type': 'select',
                'query': "SELECT * FROM customers_info WHERE customers_info_id IN " + self.list_to_in_condition(
                    customer_ids)
            },
        }

        customers_ext = self.select_multiple_data_connector(customer_ext_queries, 'customers_info')
        if not customers_ext or customers_ext['result'] != 'success':
            return response_error('Error customers ext data')

        country_ids = duplicate_field_value_from_list(customers_ext['data']['address_book'], 'entry_country_id')
        state_ids = duplicate_field_value_from_list(customers_ext['data']['address_book'], 'entry_zone_id')
        customers_ext_rel_queries = {
            'countries': {
                'type': 'select',
                'query': "SELECT * FROM countries WHERE countries_id IN " + self.list_to_in_condition(country_ids)
            },
            'zones': {
                'type': 'select',
                'query': "SELECT * FROM zones WHERE zone_id IN " + self.list_to_in_condition(state_ids)
            },
        }

        customers_ext_rel = self.select_multiple_data_connector(customers_ext_rel_queries, 'customers')
        if not customers_ext_rel or customers_ext_rel['result'] != 'success':
            return response_error('err customers ext rel data')
        customers_ext = self.sync_connector_object(customers_ext, customers_ext_rel)
        return customers_ext

    def convert_customer_export(self, customer, customers_ext):
        customer_data = self.construct_customer()


        customer_data['username'] = customer['customers_email_address']
        customer_data['email'] = customer['customers_email_address']
        customer_data['password'] = customer['customers_password']
        customer_data['first_name'] = customer['customers_firstname']
        customer_data['last_name'] = customer['customers_lastname']
        customer_data['gender'] = customer['customers_gender']
        customer_data['dob'] = customer['customers_dob']
        customer_data['telephone'] = customer['customers_telephone']
        customer_data['fax'] = customer['customers_fax']
        # customer_data['created_at']=convert_format_time(customers_ext['data']['customers_info']['customers_info_date_account_created'])
        # customer_data['updated_at']=convert_format_time(customers_ext['data']['customers_info']['customers_info_date_account_last_modified'])
        customer_data['active'] = True


        address_books = get_list_from_list_by_field(customers_ext['data']['address_book'], 'customers_id',
                                                    customer['customers_id'])
        if address_books:
            for address_book in address_books:
                address_data = self.construct_customer_address()
                address_data['id'] = address_book['address_book_id']
                address_data['first_name'] = address_book['entry_firstname']
                address_data['last_name'] = address_book['entry_lastname']
                address_data['gender'] = address_book['entry_gender']
                address_data['address_1'] = address_book['entry_street_address']
                address_data['address_2'] = ""
                address_data['city'] = address_book['entry_city']
                address_data['postcode'] = address_book['entry_postcode']
                address_data['telephone'] = customer['customers_telephone']
                address_data['fax'] = customer['customers_fax']

                country = get_row_from_list_by_field(customers_ext['data']['countries'], 'countries_id',
                                                     address_book['entry_country_id'])
                if country:
                    address_data['country']['id'] = country['countries_id']
                    address_data['country']['country_code'] = country['countries_iso_code_2']
                    address_data['country']['name'] = country['countries_name']

                else:
                    address_data['country']['id'] = address_book['entry_country_id']
                state_id = address_book['entry_state']

                if state_id:
                    state = get_row_from_list_by_field(customers_ext['data']['zones'], 'zone_code', state_id)
                    if state:
                        address_data['state']['id'] = state['zone_id']
                        address_data['state']['state_code'] = state['zone_code']
                        address_data['state']['name'] = state['zone_name']

                    else:
                        address_data['state']['id'] = state_id
                        address_data['state']['name'] = 'Alabama'
                else:
                    address_data['state']['name'] = 'AL'
                if address_book['address_book_id'] == customer['customers_default_address_id']:
                    address_data['default']['billing'] = True
                    address_data['default']['shipping'] = True
                customer_data['address'].append(address_data)
        return response_success(customer_data)

    def get_customer_id_import(self, convert, customer, customers_ext):
        return customer['customers_id']

    def check_customer_import(self, convert, customer, customers_ext):
        return True if self.get_map_field_by_src(self.TYPE_CUSTOMER, convert['customers_id'],
                                                 convert['code']) else False

    def router_customer_import(self, convert, customer, customers_ext):
        return response_success('customer_import')

    def before_customer_import(self, convert, customer, customers_ext):
        return response_success()

    def customer_import(self, convert, customer, customers_ext):
        return response_success()

    def after_customer_import(self, customer_id, convert, customers_ext):
        return response_success()

    def addition_customer_import(self, convert, customer, customers_ext):
        return response_success()

    # TODO: ORDER

    def prepare_orders_import(self):
        return self

    def prepare_orders_export(self):
        return self

    def get_orders_main_export(self):
        id_src = self._notice['process']['orders']['id_src']
        limit = self._notice['setting']['orders']
        query = {
            'type': 'select',
            'query': "SELECT * FROM orders WHERE orders_id > " + to_str(
                id_src) + " ORDER BY orders_id ASC LIMIT " + to_str(limit)
        }

        orders = self.get_connector_data(self.get_connector_url('query'), {'query': json.dumps(query)})
        if not orders or orders['result'] != 'success':
            return response_error('Could not get orders main to export')
        return orders

    def get_orders_ext_export(self, orders):
        url_query = self.get_connector_url('query')
        order_ids = duplicate_field_value_from_list(orders['data'], 'orders_id')
        bil_country = duplicate_field_value_from_list(orders['data'], 'bill_cntry')
        delivery_country = duplicate_field_value_from_list(orders['data'], 'ship_cntry')
        country_ids = set(bil_country + delivery_country)

        payment_zone = duplicate_field_value_from_list(orders['data'], 'bill_state')
        shipping_zone = duplicate_field_value_from_list(orders['data'], 'ship_state')

        state_ids = set(payment_zone + shipping_zone)
        cus_ids = duplicate_field_value_from_list(orders['data'], 'cust_id')
        orders_ext_queries = {
            'orders_products': {
                'type': 'select',
                'query': "SELECT * FROM orders_products WHERE orders_id IN " + self.list_to_in_condition(order_ids)
            },
            'orders_total': {
                'type': 'select',
                'query': "SELECT * FROM orders_total WHERE orders_id IN " + self.list_to_in_condition(order_ids)
            }
        }
        orders_ext = self.select_multiple_data_connector(orders_ext_queries, "orders")
        if not orders_ext or orders_ext['result'] != 'success':
            return response_error()
        return orders_ext

    def convert_order_export(self, order, orders_ext):
        total= 0.0
        for item in orders_ext['data']['orders_total']:
            if item['class'] == 'ot_total' and item['orders_id']==order['orders_id']:
                total = to_decimal(float(item['value']))

        self.log(order,"order")
        self.log(orders_ext,"orders_ext")
        order_data = self.construct_order()
        order_data['id'] = order['orders_id']
        order_data['status'] = order['orders_status']

        order_data['tax']['title'] = 'Tax'
        order_data['tax']['amount'] = get_value_by_key_in_dict(order, 'total_tax', 0.0000)
        order_data['shipping']['title'] = 'Shipping'
        order_data['shipping']['amount'] = get_value_by_key_in_dict(order, 'total_ship', 0.0000)
        order_data['discount']['title'] = 'Discount'
        order_data['discount']['amount'] = 0.0000
        order_data['total']['title'] = get_value_by_key_in_dict(orders_ext['data']['orders_total'], 'title')
        # begin test block
        order_data['total']['amount'] = total
        # end of test block
        self.log(order_data['total']['amount'],"total_amount")
        order_data['subtotal']['title'] = 'Total products'
        order_data['subtotal']['amount'] = get_value_by_key_in_dict(order, 'total', 0.0000)
        order_data['currency'] = order['currency']
        order_data['created_at'] = order['date_purchased']
        order_data['updated_at'] = get_current_time()

        order_customer = self.construct_order_customer()
        order_customer['id'] = order['client_orders_id']
        order_customer['email'] = order['customers_email']
        customer_name = order['billing_name']

        order_data['customer'] = order_customer

        customer_address = self.construct_order_address()
        customer_address['address_1'] = order['delivery_address1']
        customer_address['address_2'] = order['delivery_address2']
        customer_address['city'] = order['delivery_city']
        customer_address['postcode'] = order['delivery_postcode']
        customer_address['telephone'] = order['customers_telephone']
        customer_address['company'] = order['delivery_company']
        customer_address['state']['name'] = order['delivery_state']
        customer_address['country']['name'] = order['delivery_country']

        order_data['customer_address'] = customer_address
        order_billing = self.construct_order_address()

        billing_name = order['billing_name']

        order_billing['address_1'] = order['billing_address1']
        order_billing['address_2'] = order['billing_address2']
        order_billing['first_name'] = ((order['billing_name']).split(" "))[0]
        order_billing['last_name'] = ((order['billing_name']).split(" "))[1]
        order_billing['city'] = order['billing_city']
        order_billing['postcode'] = order['delivery_postcode']
        order_billing['telephone'] = order['customers_telephone']
        order_billing['company'] = order['billing_company']

        order_billing['country']['name'] = order['billing_country']
        order_billing['state']['name'] = order['billing_state']

        order_data['billing_address'] = order_billing

        order_delivery = self.construct_order_address()

        delivery_name = order['delivery_name']

        order_delivery['address_1'] = order['delivery_address1']
        order_delivery['address_2'] = order['delivery_address2']
        order_delivery['city'] = order['delivery_city']
        order_delivery['postcode'] = order['delivery_postcode']
        order_delivery['telephone'] = order['delivery_postcode']
        order_delivery['company'] = order['order_number']

        order_delivery['country']['name'] = order['delivery_country']
        order_delivery['state']['state'] = order['delivery_state']

        order_delivery = self._cook_shipping_address_by_billing(order_delivery, order_billing)
        order_data['shipping_address'] = order_delivery

        order_products = get_list_from_list_by_field(orders_ext['data']['orders_products'], 'orders_id',
                                                     order['orders_id'])

        order_items = list()
        for order_product in order_products:
            order_item_subtotal = to_decimal(order_product['products_price']) * to_decimal(
                order_product['products_quantity'])
            order_item_tax = to_decimal(order_item_subtotal) * to_decimal(8.250) / 100
            order_item_total = to_decimal(order_item_subtotal) + to_decimal(order_item_tax)
            order_item = self.construct_order_item()
            order_item['id'] = order_product['orders_products_id']
            order_item['product']['id'] = order_product['orders_products_id']
            order_item['product']['name'] = order_product['products_name']
            order_item['qty'] = order_product['products_quantity']
            order_item['price'] = order_product['products_price']
            order_item['original_price'] = order_product['final_price']
            order_item['discount_amount'] = '0.0000'
            order_item['discount_percent'] = '0.0000'
            order_item['subtotal'] = order_item_subtotal
            order_item['total'] = order_item_subtotal
            order_items.append(order_item)

        order_data['items'] = order_items
        return response_success(order_data)

    def get_order_id_import(self, convert, order, orders_ext):
        return order['orders_id']

    def check_order_import(self, convert, order, orders_ext):
        return True if self.get_map_field_by_src(self.TYPE_ORDER, convert['orders_id'], convert['code']) else False

    def router_order_import(self, convert, order, orders_ext):
        return response_success('order_import')

    def before_order_import(self, convert, order, orders_ext):
        return response_success()

    def order_import(self, convert, order, orders_ext):
        return response_success(0)

    def after_order_import(self, order_id, convert, order, orders_ext):
        return response_success()

    def addition_order_import(self, convert, order, orderes_ext):
        return response_success()

    # TODO: PAGE
    def prepare_pages_import(self):
        return self

    def prepare_pages_export(self):
        return self

    def get_pages_main_export(self):
        return response_success()

    def get_pages_ext_export(self, pages):
        return response_success()

    def convert_page_export(self, page, pages_ext):
        return response_success()

    def get_page_id_import(self, convert, page, pages_ext):
        return False

    def check_page_import(self, convert, page, pages_ext):
        return False

    def router_page_import(self, convert, page, pages_ext):
        return response_success('page_import')

    def before_page_import(self, convert, page, pages_ext):
        return response_success()

    def page_import(self, convert, page, pages_ext):
        return response_success(0)

    def after_page_import(self, page_id, convert, page, pages_ext):
        return response_success()

    def addition_page_import(self, convert, page, pages_ext):
        return response_success()

    # TODO: BLOCK
    def prepare_blogs_import(self):
        return response_success()

    def prepare_blogs_export(self):
        return self

    def get_blogs_main_export(self):
        return self

    def get_blogs_ext_export(self, blocks):
        return response_success()

    def convert_blog_export(self, block, blocks_ext):
        return response_success()

    def get_blog_id_import(self, convert, block, blocks_ext):
        return False

    def check_blog_import(self, convert, block, blocks_ext):
        return False

    def router_blog_import(self, convert, block, blocks_ext):
        return response_success('block_import')

    def before_blog_import(self, convert, block, blocks_ext):
        return response_success()

    def blog_import(self, convert, block, blocks_ext):
        return response_success(0)

    def after_blog_import(self, block_id, convert, block, blocks_ext):
        return response_success()

    def addition_blog_import(self, convert, block, blocks_ext):
        return response_success()

    # TODO: OPENCART

    def _list_to_in_condition_product(self, products):
        if not products:
            return "('null')"

        products = list(map(self.escape, products))
        products = list(map(lambda x: to_str(x), products))
        res = "',' product_id = ".join(products)
        res = "('product_id=" + res + "')"
        return res

    def product_to_in_condition_seourl(self, ids):
        if not ids:
            return "('null')"
        result = "('product_id=" + "','product_id=".join([str(id) for id in ids]) + "')"
        return result

    def category_to_in_condition_seourl(self, ids):
        if not ids:
            return "('null')"
        result = "('category_id=" + "','category_id=".join([str(id) for id in ids]) + "')"
        return result

    def get_category_parent(self, category_id):
        query = {
            'type': 'select',
            'query': "SELECT * FROM categories WHERE categories_id = " + to_str(category_id)
        }
        categories = self.select_data_connector(query, 'categories')
        if not categories or categories['result'] != 'success':
            return response_error('Could not get category parent to export')
        if categories and categories['data']:
            category = categories['data'][0]
            categories_ext = self.get_categories_ext_export(categories)
            category_convert = self.convert_category_export(category, categories_ext)
            return category_convert
        return response_error('Could not get category parent to export')

    def import_category_parent(self, convert_parent):
        parent_exists = self.get_map_field_by_src(self.TYPE_CATEGORY, convert_parent['id'], convert_parent['code'])
        if parent_exists:
            return response_success(parent_exists)
        category = convert_parent['category']
        categories_ext = convert_parent['categories_ext']
        category_parent_import = self.category_import(convert_parent, category, categories_ext)
        self.after_category_import(category_parent_import['data'], convert_parent, category, categories_ext)
        return category_parent_import

    def nl2br(self, string, is_xhtml=True):
        if is_xhtml:
            return string.replace('\n', '<br />\n')
        else:
            return string.replace('\n', '<br>\n')

    def get_country_id(self, code, name):
        query = "SELECT country_id FROM countries"
        if code:
            query = query + ' WHERE countries_iso_code_2 = "' + to_str(code) + '"'
        elif name:
            query = query + ' WHERE name = "' + to_str(name) + '"'
        countries_query = {
            'type': 'select',
            'query': query
        }

        countries = self.get_connector_data(self.get_connector_url('query'), {'query': json.dumps(countries_query)})
        if not countries or countries['result'] != 'success' or not countries['data']:
            return 0
        return countries['data'][0]['country_id']

    def get_state_id(self, code, name):
        query = 'SELECT zone_id FROM zones'
        if code:
            query = query + ' WHERE code = "' + to_str(code) + '"'
        elif name:
            query = query + ' WHERE code = "' + to_str(name) + '"'
        countries_query = {
            'type': 'select',
            'query': query
        }
        countries = self.get_connector_data(self.get_connector_url('query'), {'query': json.dumps(countries_query)})
        if not countries or countries['result'] != 'success' or not countries['data']:
            return 0
        return countries['data'][0]['country_id']

    def get_state_id(self, code, name):
        query = 'SELECT zone_id FROM zones'
        if code:
            query = query + ' WHERE code = "' + to_str(code) + '"'
        elif name:
            query = query + ' WHERE name = "' + to_str(name) + '"'
        zones_query = {
            'type': 'select',
            'query': query
        }
        zones = self.get_connector_data(self.get_connector_url('query'), {'query': json.dumps(zones_query)})
        if not zones or zones['result'] != 'success' or not zones['data']:
            return 0
        return zones['data'][0]['zone_id']

    def calculate_average_rating(self, rates, default='default'):
        rate = get_row_from_list_by_field(rates, 'rate_code', default)
        if rate and 'rate' in rate:
            return rate['rate']
        rate_total = 0
        count = to_len(rates)
        for _rate in rates:
            rate_total = rate_total + to_decimal_rate(['rate'])
        average = to_decimal(rate_total / count)
        if average > 5:
            return 5
        else:
            return math.ceil(average)

    def get_name_from_string(self, value):
        result = dict()
        parts = value.split(' ')
        result['lastname'] = parts.pop()
        result['firstname'] = " ".join(parts)
        return result

    def _cook_shipping_address_by_billing(self, shipping_address, billing_address):
        for key, value in shipping_address.items():
            if key in {'country', 'state'}:
                for child_key, child_value in shipping_address[key].items():
                    if not shipping_address[key][child_key]:
                        shipping_address[key][child_key] = billing_address[key][child_key]
            else:
                if not shipping_address[key]:
                    shipping_address[key] = billing_address[key]
        return shipping_address

    def convert_float_to_percent(self, value):
        return value * 100

    def get_con_store_select(self):
        select_store = self._notice['src']['languages_select'].copy()
        src_store = self._notice['src']['languages'].copy()
        if self._notice['src']['language_default'] not in select_store:
            select_store.append(self._notice['src']['language'])
        src_store_ids = list(src_store.keys())
        unselect_store = [item for item in src_store_ids if item not in select_store]
        select_store.append(0)
        if to_len(select_store) >= to_len(unselect_store):
            where = ' IN ' + self.list_to_in_condition(select_store) + ' '
        else:
            where = ' NOT IN ' + self.list_to_in_condition(unselect_store) + ' '
        return where

    def detect_seo(self):
        return 'default_seo'

    def categories_default_seo(self, category, categories_ext):
        result = list()
        type_seo = self.SEO_301
        category_url = get_list_from_list_by_field(categories_ext['data']['URIs'], 'cat_id', category['id'])
        seo_cate = self.construct_seo_category()
        if category_url:
            for cate_url in category_url:
                seo_cate['request_path'] = cate_url['uri']
                seo_cate['default'] = True
                seo_cate['type'] = type_seo
                result.append(seo_cate)

        return result

    def products_default_seo(self, product, products_ext):
        result = list()
        type_seo = self.SEO_301
        category_url = get_list_from_list_by_field(products_ext['data']['URIs'], 'cat_id', product['id'])
        seo_cate = self.construct_seo_product()
        if category_url:
            for cate_url in category_url:
                seo_cate['request_path'] = cate_url['uri']
                seo_cate['default'] = True
                seo_cate['type'] = type_seo
                result.append(seo_cate)

        return result

    def to_url(self, name):
        new_name = re.sub(r"[^a-zA-Z0-9-. ]", '', name)
        new_name = new_name.replace(' ', '-')
        url = new_name.lower()
        return url
