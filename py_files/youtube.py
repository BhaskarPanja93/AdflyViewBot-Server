def run(local_ip):
    def write_current_occurance(string):
        f=open(f"host side\\static\\{local_ip} current.txt",'a')
        f.write(str(time.ctime())+' : '+string+'\n')
        f.close()
    def write_debug_occurance(string):
        unique_id=random.randrange(1,10000)
        f=open(f"debugging captures\\{local_ip}.txt",'a')
        f.write(str(time.ctime())+' : '+string+' : '+str(unique_id)+'\n')
        f.close()
        iml=pyautogui.screenshot()
        iml.save(f"debugging captures\\{unique_id}.png")

        
    comment=''
    import time
    import pyautogui
    import random
    import threading
    import subprocess
    import os
    import pyperclip
    globals()['last_change_condition']=''
    globals()['last_change_timing']=time.time()
    globals()['success']=False
    globals()['failure']=False
    screen_x,screen_y=pyautogui.size()
    img_location='req_imgs\\'
    extension='.png'
    pyautogui.FAILSAFE=False
    mouse_movement_speed=0.4
    typing_speed=0.06
    pyautogui.click(screen_x,screen_y-5)
    globals()['possible_screen_conditions']={
        'force_click':['adfly continue', 'go to site'],
        'force_close_chrome':['yt video private', 'yt video unavailable','cookies not enabled','adfly suspended'],
        'proton vpn minimise':['protonvpn ad region'],
        #'chrome_restore':['chrome restore'],
        'nothing_opened':['chrome icon'],
        #'chrome_ad':['chrome ads region 1', 'chrome ads region 2'],
        'blank_chrome':['search box 1', 'search box 2', 'search box 3', 'search box 4'],
        'google_captcha':['google captcha'],
        'youtube_proxy_detected':['before you continue to youtube en'],
        'youtube_popup':['yt popup 1 dismiss', 'yt popup 2 dismiss'],
        'youtube_open':['yt show more','yt share'],
        'adfly_skip':['adfly skip'],
        #'click here to continue':['click here to continue region'],
        'click allow to continue':['click allow to continue']
        }

    def temp_remove_possibility(item,duration):
        data=globals()['possible_screen_conditions'][item]
        globals()['possible_screen_conditions'][item]=[]
        if duration!=0:
            time.sleep(duration)
            globals()['possible_screen_conditions'][item]=data


    while not globals()['success'] and not globals()['failure']:
        time.sleep(1)
        condition_found=False            
        try:
            del current_screen_condition
        except:
            pass
        if time.time()-globals()['last_change_timing']>3*60:
            current_screen_condition='force_close_chrome'
            globals()['last_change_timing']=time.time()
        else:
            for condition in possible_screen_conditions:
                if not condition_found:
                    for sign in possible_screen_conditions[condition]:
                        coordinates=pyautogui.locateOnScreen(img_location+sign+extension, confidence=0.8)
                        if coordinates!=None:
                            current_screen_condition=condition
                            condition_found=True
                            x,y,x_thick,y_thick=coordinates
                            x+=x_thick//2
                            y+=y_thick//2
                            break
        
        if 'current_screen_condition' in dir():
            if current_screen_condition != globals()['last_change_condition']:
                globals()['last_change_timing']=time.time()
                globals()['last_change_condition']=current_screen_condition
            write_current_occurance(current_screen_condition)
            print(current_screen_condition)
            if current_screen_condition == 'force_click':#####
                pyautogui.moveTo(x,y,mouse_movement_speed)
                pyautogui.click(x,y)
                write_current_occurance('force clicked')
            elif current_screen_condition == 'proton vpn minimise':#####
                sign='protonvpn ad close'
                coordinates=pyautogui.locateOnScreen(img_location+sign+extension,region=coordinates, confidence=0.8)
                if coordinates!=None:
                    x,y=pyautogui.center(coordinates)
                    pyautogui.moveTo(x,y,mouse_movement_speed)
                    pyautogui.click(x,y)
                    write_current_occurance('protonvpn minimised')
            elif current_screen_condition=='chrome_ad':#####
                x+=x_thick//2
                pyautogui.moveTo(x,y,mouse_movement_speed)
                pyautogui.click(x,y)
##                sign='chrome ads close'
##                ad_close_coords=pyautogui.locateOnScreen(img_location+sign+extension, region=coordinates, confidence=0.9)
##                if ad_close_coords!=None:
##                    print('ad_close_button_found')
##                    x,y=pyautogui.center(ad_close_coords)
##                    pyautogui.moveTo(x,y,mouse_movement_speed)
##                    pyautogui.click(x,y)
            elif current_screen_condition=='chrome_restore':#####
                sign='chrome restore close'
                close_coordinates=pyautogui.locateOnScreen(img_location+sign+extension,region=coordinates, confidence=0.9)
                if close_coordinates!=None:
                    x,y=pyautogui.center(coordinates)
                    pyautogui.moveTo(x,y,mouse_movement_speed)
                    pyautogui.click(x,y)
                    write_current_occurance('chrome restore closed')
            elif current_screen_condition == 'nothing_opened':#####
                threading.Thread(target=temp_remove_possibility, args=(current_screen_condition,120,)).start()
                pyautogui.moveTo(x,y,mouse_movement_speed)
                pyautogui.doubleClick(x,y)
                write_current_occurance('chrome opened')
            elif current_screen_condition == 'blank_chrome':#####
                temp_remove_possibility('blank_chrome',60)
                f=open('my_links.txt','r')
                main_link=random.choice(f.read().split('\n'))
                for sign in ['search box 1', 'search box 2', 'search box 3', 'search box 4']:
                    coordinates=pyautogui.locateOnScreen(img_location+sign+extension, confidence=0.8)
                    if coordinates!=None:
                        x,y=pyautogui.center(coordinates)
                        pyautogui.moveTo(x,y,mouse_movement_speed)
                        pyautogui.click(x,y)
                        pyautogui.hotkey('ctrl','a')
                        time.sleep(2)
                        pyautogui.typewrite(main_link,typing_speed)
                        time.sleep(2)
                        pyautogui.press('enter')
                        write_current_occurance('site reached')
                        break
            elif current_screen_condition == 'google_captcha':#####
                globals()['failure']=True
                globals()['comment']='change_ip'
            elif current_screen_condition == 'youtube_proxy_detected':#####
                pyautogui.moveTo(x,y,mouse_movement_speed)
                pyautogui.click(x,y)
                scrolled_time=time.time()
                while time.time()-scrolled_time<=2:
                    pyautogui.scroll(-20)
                write_current_occurance('yt proxy scrolled')
                i_agree_signs=['yt proxy i agree en']
                for sign in i_agree_signs:
                    coordinates=pyautogui.locateOnScreen(img_location+sign+extension, confidence=0.8)
                    if coordinates!=None:
                        x,y=pyautogui.center(coordinates)
                        pyautogui.moveTo(x,y,mouse_movement_speed)
                        pyautogui.click(x,y)
                        write_current_occurance('yt proxy agreed')
                        break
                globals()['comment']='change_ip'
            elif current_screen_condition == 'youtube_popup':#####
                pyautogui.moveTo(x,y,mouse_movement_speed)
                pyautogui.click(x,y)
                write_current_occurance('yt popup closed')
            elif current_screen_condition == 'youtube_open':#####
                pyautogui.moveTo(x,y, mouse_movement_speed)
                sign='yt share'
                scrolled_time=time.time()
                while pyautogui.locateOnScreen(img_location+sign+extension, confidence=0.7)!=None and time.time()-scrolled_time<=6:
                    pyautogui.moveTo(screen_x//2,screen_y//2, mouse_movement_speed)
                    pyautogui.scroll(-50)
                write_current_occurance('yt scrolled')
                sign='yt show more'
                coordinates=pyautogui.locateOnScreen(img_location+sign+extension, confidence=0.7)
                if coordinates!=None:
                    x,y=pyautogui.center(coordinates)
                    pyautogui.moveTo(x,y,mouse_movement_speed)
                    pyautogui.click(x,y)
                    write_current_occurance('yt show more')
                available_links=[]
                sign='link initial'
                for link in pyautogui.locateAllOnScreen(img_location+sign+extension, confidence=0.8):
                    available_links.append(link)
                write_current_occurance(str(len(available_links))+' links found')
                if len(available_links)>0:
                    x,y=pyautogui.center(random.choice(available_links))
                    pyautogui.moveTo(x,y,mouse_movement_speed)
                    pyautogui.click(x,y)
                    write_current_occurance('link clicked')
                else:
                    sign='chrome close region'
                    chrome_close_region=pyautogui.locateOnScreen(img_location+sign+extension, confidence=0.7)
                    sign='chrome close'
                    coordinates=pyautogui.locateOnScreen(img_location+sign+extension,region=chrome_close_region, confidence=0.7)
                    if coordinates!=None:
                        x,y=pyautogui.center(coordinates)
                        pyautogui.moveTo(x,y,mouse_movement_speed)
                        pyautogui.click(x,y)
                        globals()['success']=True
                        write_current_occurance('found no link, closed')
            elif current_screen_condition == 'adfly_skip':#####
                items=['yt tab playing','yt tab paused']
                for sign in items:
                    yt_close_region=pyautogui.locateOnScreen(img_location+sign+extension, confidence=0.7)
                    if yt_close_region!=None:
                        break
                sign='yt tab close'
                yt_tab_close=pyautogui.locateCenterOnScreen(img_location+sign+extension,region=yt_close_region, confidence=0.7)
                if yt_tab_close!=None:
                    yt_tab_close_x,yt_tab_close_y=yt_tab_close
                    pyautogui.moveTo(yt_tab_close_x,yt_tab_close_y,mouse_movement_speed)
                    pyautogui.click(yt_tab_close_x,yt_tab_close_y)
                    write_current_occurance('yt tab closed')
                pyautogui.moveTo(x,y,mouse_movement_speed)
                pyautogui.click(x,y)
                write_current_occurance('adfly skipped')
            elif current_screen_condition == 'click here to continue':#####
                sign='click here to continue'
                coordinates=pyautogui.locateOnScreen(img_location+sign+extension,region=coordinates, confidence=0.7)
                if coordinates!=None:
                    x,y=pyautogui.center(coordinates)
                    pyautogui.moveTo(x,y,mouse_movement_speed)
                    pyautogui.click(x,y)
            elif current_screen_condition == 'click allow to continue':#####
                sign='popup allow'
                time.sleep(2)
                coordinates=pyautogui.locateOnScreen(img_location+sign+extension, confidence=0.7)
                if coordinates!=None:
                    x,y=pyautogui.center(coordinates)
                    pyautogui.moveTo(x,y,mouse_movement_speed)
                    pyautogui.click(x,y)
            elif current_screen_condition == 'force_close_chrome':#####
                write_current_occurance('force close chrome')
                write_debug_occurance('force close chrome')
                sign='chrome close region'
                chrome_close_region=pyautogui.locateOnScreen(img_location+sign+extension, confidence=0.7)
                sign='chrome close'
                coordinates=pyautogui.locateOnScreen(img_location+sign+extension,region=chrome_close_region, confidence=0.7)
                if coordinates!=None:
                    write_current_occurance('chrome closed')
                    x,y=pyautogui.center(coordinates)
                    pyautogui.moveTo(x,y,mouse_movement_speed)
                    pyautogui.click(x,y)
                    write_current_occurance('chrome closed')
        else:
            random_x,random_y=random.randrange(0,100),random.randrange(0,100)
            current_x,current_y=pyautogui.position()
            if random_x+current_x>10 or random_x+current_x<screen_x-10 and random_y+current_y>10 or random_y+current_y<screen_y-10:
                pyautogui.move(random_x,random_y,mouse_movement_speed/3)
    write_current_occurance('end of instance')
    write_current_occurance('force close chrome')
    sign='chrome close region'
    chrome_close_region=pyautogui.locateOnScreen(img_location+sign+extension, confidence=0.7)
    sign='chrome close'
    coordinates=pyautogui.locateOnScreen(img_location+sign+extension,region=chrome_close_region, confidence=0.7)
    if coordinates!=None:
        write_current_occurance('chrome closed')
        x,y=pyautogui.center(coordinates)
        pyautogui.moveTo(x,y,mouse_movement_speed)
        pyautogui.click(x,y)
        write_current_occurance('chrome closed')
    
    for j in dir():
        if j!='j' and j!='success' and j!='comment':
            try:
                del globals()[j]
            except:
                pass

    if success:
        return 'youtube',1,0,comment
    else:
        return 'youtube',0,1,comment