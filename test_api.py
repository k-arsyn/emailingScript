import requests
import pandas as pd

# Test the API endpoints with a small sample
TRACKING_SERVER = "https://emailingscript-production.up.railway.app"

def test_api():
    print("🧪 Testing API endpoints...")
    
    # Test basic connection
    try:
        response = requests.get(f"{TRACKING_SERVER}/")
        print(f"✅ Server responding: {response.status_code}")
    except Exception as e:
        print(f"❌ Server connection failed: {e}")
        return
    
    # Test campaign creation
    try:
        campaign_data = {
            "name": "Test_Campaign_API",
            "description": "Testing the API endpoints"
        }
        
        response = requests.post(f"{TRACKING_SERVER}/create-campaign", 
                               data=campaign_data)
        
        if response.status_code == 200:
            result = response.json()
            campaign_id = result.get('campaignId')
            print(f"✅ Campaign created: {campaign_id}")
            
            # Test bulk pixel creation
            test_emails = ["test1@example.com", "test2@example.com"]
            bulk_data = {
                "campaignId": campaign_id,
                "campaignName": "Test_Campaign_API",
                "emails": test_emails
            }
            
            response = requests.post(f"{TRACKING_SERVER}/create-bulk", 
                                   json=bulk_data,
                                   headers={'Content-Type': 'application/json'})
            
            if response.status_code == 200:
                result = response.json()
                pixels = result.get('pixels', [])
                print(f"✅ Created {len(pixels)} tracking pixels")
                for pixel in pixels:
                    print(f"   📊 {pixel['email']} -> {pixel['trackingUrl']}")
                return True
            else:
                print(f"❌ Bulk creation failed: {response.text}")
                return False
        else:
            print(f"❌ Campaign creation failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ API test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_api()
    if success:
        print("\n🎉 All API tests passed!")
        print(f"📊 Dashboard: {TRACKING_SERVER}")
    else:
        print("\n❌ Some tests failed. Check the error messages above.")
