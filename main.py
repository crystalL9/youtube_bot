import device_config_ultils
import work
if __name__ == "__main__":
    local_device_config = device_config_ultils.get_local_device_config()
    print(f"Mode = {local_device_config[0]['mode']['id']}")
    if local_device_config[0]['mode']['id']==1 :
        work.work_keyword(local_device_config=local_device_config)
    elif local_device_config[0]['mode']['id']==2 :
        work.work1(local_device_config=local_device_config)
    elif local_device_config[0]['mode']['id']==3 : 
        work.update(local_device_config=local_device_config)
    else:
        print("⚠ ⚠ ⚠ File config không hợp lệ ⚠ ⚠ ⚠ ")

    
