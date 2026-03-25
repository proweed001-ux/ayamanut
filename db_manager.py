import json
import os
from datetime import datetime, timedelta

# Paths to data files
STORES_FILE = 'data/stores.json'
INVENTORY_FILE = 'data/inventory.json'

def load_data(file_path):
    if not os.path.exists(file_path):
        return []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

def save_data(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def add_or_update_store(store_id, name, lat, long, zone, route, store_class=None, phone=None, address=None):
    stores = load_data(STORES_FILE)
    store_found = False
    for store in stores:
        if str(store['id']) == str(store_id):
            update_data = {
                'name': name,
                'lat': lat,
                'long': long,
                'zone': zone,
                'route': route,
                'updated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            if store_class: update_data['class'] = store_class
            if phone: update_data['phone'] = phone
            if address: update_data['address'] = address
            
            store.update(update_data)
            store_found = True
            break
    
    if not store_found:
        stores.append({
            'id': str(store_id),
            'name': name,
            'lat': lat,
            'long': long,
            'zone': zone,
            'route': route,
            'class': store_class if store_class else 'N/A',
            'phone': phone if phone else 'N/A',
            'address': address if address else 'N/A',
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
    
    save_data(STORES_FILE, stores)
    return f"อัปเดตข้อมูลร้าน {name} (ID: {store_id}) เรียบร้อยแล้ว"

def add_inventory_item(store_id, product_name, quantity, seller_name):
    inventory = load_data(INVENTORY_FILE)
    now = datetime.now()
    expiry_date = now + timedelta(days=90)
    
    item = {
        'id': f"INV_{int(now.timestamp())}",
        'store_id': str(store_id),
        'product_name': product_name,
        'quantity': quantity,
        'seller_name': seller_name,
        'created_at': now.strftime('%Y-%m-%d %H:%M:%S'),
        'expiry_date': expiry_date.strftime('%Y-%m-%d')
    }
    
    inventory.append(item)
    save_data(INVENTORY_FILE, inventory)
    return f"บันทึกสินค้า {product_name} สำหรับร้าน {store_id} เรียบร้อยแล้ว (หมดอายุ {expiry_date.strftime('%Y-%m-%d')})"

def cleanup_expired_items():
    inventory = load_data(INVENTORY_FILE)
    today = datetime.now().strftime('%Y-%m-%d')
    new_inventory = [item for item in inventory if item['expiry_date'] >= today]
    
    if len(inventory) != len(new_inventory):
        save_data(INVENTORY_FILE, new_inventory)
        return f"ลบสินค้าที่หมดอายุแล้ว {len(inventory) - len(new_inventory)} รายการ"
    return "ไม่มีสินค้าหมดอายุ"

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "cleanup":
            print(cleanup_expired_items())
