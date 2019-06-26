import sys
import os

class LCD_conf:
    Config_File = '/boot/config.txt'

    max_usb_current = '1'

    #  Config data for 5 inched LCD
    lcd5in = [
                'hdmi_group=2',
                'hdmi_mode=87',
                'hdmi_cvt 800 480 60 6 0 0 0'
                ]

    #  Config data for 7 inches LCD
    lcd7in = [
                'hdmi_force_hotplug=1',
                'config_hdmi_boost=10',
                'hdmi_group=2',
                'hdmi_mode=87',
                'hdmi_cvt 1024 600 60 6 0 0 0'
                ]
	
    def read_file(self):
        '''
        Read config.txt file in python list
        '''
        with open(self.Config_File) as conf_file:
            conf_file = conf_file.read()
            lines = conf_file.split('\n')
        return lines

    def modify_data(self, display_size = 5, display_rotate = 0):
        '''
        Edit file data and return list
        '''
        if display_size is not None:
            file_data = self.read_file()
            index_delete = []
            for line in file_data:
                if 'hdmi' in line:
                    if ('hdmi_group' in line):
                        index_delete.append(file_data.index(line))
                    elif 'hdmi_cvt' in line:
                        index_delete.append(file_data.index(line))
                    elif 'hdmi_mode' in line:
                        index_delete.append(file_data.index(line))
                    elif 'hdmi_force_hotplug' in line:
                        index_delete.append(file_data.index(line))

                if 'max_usb_current' in line:
                    index_delete.append(file_data.index(line))

                if 'config_hdmi_boost' in line:
                    index_delete.append(file_data.index(line))

                if 'display_rotate' in line:
                    index_delete.append(file_data.index(line))
                    
            for ind in reversed(index_delete):
                del file_data[ind]
            del file_data[len(file_data) - 1]
    		
            file_data.append('max_usb_current=' + self.max_usb_current)
            if display_size == 5:
                display = self.lcd5in
            elif display_size == 7:
                display = self.lcd7in
                                
            for line in display:
                file_data.append(line)

            if display_rotate in [1, 2, 3]:
                file_data.append('display_rotate={}'.format(display_rotate))  #  1: 90; 2: 180; 3: 270
            
            return file_data

    def write_file(self):
        '''
        Write data to config.txt file
        '''
        if len(sys.argv) > 1:
            size = int(sys.argv[1])
            rotation = int(sys.argv[2]) if len(sys.argv) > 2 else 0
        else:
            size = None
            rotation = None
        data_to_write = self.modify_data(display_size = size, display_rotate = int(rotation/90))

        with open(self.Config_File, 'w') as conf_file:
            for item in data_to_write:
                conf_file.write(item+'\n' )
        print('Reboot to apply changes.\n')
        reboot = input("Do you want to reboot?\t('y'|'n')\t")
        while not reboot:
            reboot = input("Do you want to reboot?\t('y'|'n')\t")
        if reboot in ['Y','y']:
            os.system('reboot')

if __name__ == '__main__':
    lcd = LCD_conf()
    lcd.write_file()
	
	
