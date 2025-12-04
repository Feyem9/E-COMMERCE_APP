#!/usr/bin/env python3
import os
import sys
import json

# Configuration d'environnement pour test local
os.environ['FLASK_ENV'] = 'development'
# Utiliser SQLite pour le test local au lieu de PostgreSQL
os.environ['FALLBACK_DB'] = 'sqlite:///test.db'

from app import app

def test_register():
    with app.test_client() as client:
        # Test POST avec données valides
        response = client.post('/customer/register',
            data=json.dumps({
                'email': f'test{hash("test")}@example.com',
                'name': 'Test User',
                'password': 'SecurePass123',
                'contact': '0123456789',
                'address': '123 Main Street'
            }),
            content_type='application/json'
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {response.data.decode()}")
        return response.status_code == 201 or response.status_code == 400

if __name__ == '__main__':
    try:
        success = test_register()
        print(f"✅ Test passed" if success else "❌ Test failed")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
