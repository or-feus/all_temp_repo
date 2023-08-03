class SOC_ICD():
    # ICD 14BYTE DATA
    SOURCE_CONSOLE_CONTROL_MSG = b'\x01'
    SOURCE_CONSOLE_TERMINAL_MSG = b'\x02'
    SOURCE_CONSOLE_SOC_MSG = b'\x03'
    DEST_CONSOLE_CONTROL_MSG = b'\x01'

    DEST_CONSOLE_TERMINAL_MSG = b'\x02'
    DEST_CONSOLE_SOC_MSG = b'\x03'
    THERMAL_IMAGE_DEBUG_MSG = b'\xC5'
    THERMAL_IMAGE_APP_SETTING_MSG = b'\xD0'
    THERMAL_IMAGE_USECASE_SETTING_MSG = b'\xD1'
    THERMAL_IMAGE_I2C_WRITE_MSG = b'\xB0'
    THERMAL_IMAGE_I2C_READ_MSG = b'\xB1'
    THERMAL_IMAGE_I2C_DET_SETTING_MSG = b'\xB2'
    THERMAL_IMAGE_I2C_DET_SETTING_READ_MSG = b'\xB3'
    THERMAL_IMAGE_TEC_REF_GAIN_SETTING_WRITE_MSG = b'\xB4'
    THERMAL_IMAGE_TEC_REF_OFFSET_SETTING_WRITE_MSG = b'\xB5'
    THERMAL_IMAGE_PROCESSOR_END_MSG = b'\xFF'
    THERMAL_IMAGE_I2C_ISP_SET_ADDR1 = b'\xA0'
    THERMAL_IMAGE_I2C_ISP_SET_ADDR2 = b'\xA1'
    THERMAL_IMAGE_I2C_ISP_SET_DATA1 = b'\xA2'
    THERMAL_IMAGE_I2C_ISP_SET_DATA2 = b'\xA3'
    THERMAL_IMAGE_I2C_ISP_SET_READ1 = b'\xA4'
    THERMAL_IMAGE_I2C_ISP_SET_READ2 = b'\xA5'
    THERMAL_IMAGE_AUTO_NUC_SEND_MSG = b'\xA6'
    THERMAL_IMAGE_CONT_BRIGHT_MSG = b'\x38'
    #UPDATE NEW LIST
    THERMAL_IMAGE_TRSM_GUIDE_MSG = b'\xD6'
    SEND_ICD = {
        'OPERATE_MODE' : {
            'CONSOLE_SOURCE' : SOURCE_CONSOLE_CONTROL_MSG,
            'CONSOLE_DESTINATION' : DEST_CONSOLE_SOC_MSG,
            'CONSOLE_HEADER' : THERMAL_IMAGE_DEBUG_MSG,
            'Addr' : b'\x00',
            'data' : b'\x00'
        },
        'PROCESS_END' : {
            'CONSOLE_SOURCE' : SOURCE_CONSOLE_CONTROL_MSG,
            'CONSOLE_DESTINATION' : DEST_CONSOLE_SOC_MSG,
            'CONSOLE_HEADER' : THERMAL_IMAGE_PROCESSOR_END_MSG,
            'Addr' : b'\x00',
            'data' : b'\x00'
        },
        'DEBUG_MODE': {
            'CONSOLE_SOURCE': SOURCE_CONSOLE_CONTROL_MSG,
            'CONSOLE_DESTINATION': DEST_CONSOLE_SOC_MSG,
            'CONSOLE_HEADER': THERMAL_IMAGE_DEBUG_MSG,
            'Addr': b'\x00',
            'data': b'\x02'
        },
        'VIEWER_MODE': {
            'CONSOLE_SOURCE': b'\x02',
            'CONSOLE_DESTINATION': b'\x03',
            'CONSOLE_HEADER': b'\x00',
            'Addr': b'\x00',
            'data': b'\x00'
        },
        '1-REF_NUC': {
            'CONSOLE_SOURCE': SOURCE_CONSOLE_CONTROL_MSG,
            'CONSOLE_DESTINATION': DEST_CONSOLE_SOC_MSG,
            'CONSOLE_HEADER': THERMAL_IMAGE_APP_SETTING_MSG,
            'Addr': b'\x00',
            'data': b'\x00'
        },
        'NUC_VIEW': {
            'CONSOLE_SOURCE': SOURCE_CONSOLE_CONTROL_MSG,
            'CONSOLE_DESTINATION': DEST_CONSOLE_SOC_MSG,
            'CONSOLE_HEADER': THERMAL_IMAGE_USECASE_SETTING_MSG,
            'Addr': b'\x00',
            'data': b'\x02'
        },
        'CEM_ON': {
            'CONSOLE_SOURCE': SOURCE_CONSOLE_CONTROL_MSG,
            'CONSOLE_DESTINATION': DEST_CONSOLE_SOC_MSG,
            'CONSOLE_HEADER': THERMAL_IMAGE_USECASE_SETTING_MSG,
            'Addr': b'\x00',
            'data': b'\x00'
        },
        'CEM_OFF': {
            'CONSOLE_SOURCE': SOURCE_CONSOLE_CONTROL_MSG,
            'CONSOLE_DESTINATION': DEST_CONSOLE_SOC_MSG,
            'CONSOLE_HEADER': THERMAL_IMAGE_USECASE_SETTING_MSG,
            'Addr': b'\x00',
            'data': b'\x01'
        },
        'TEC_ON': {
            'CONSOLE_SOURCE': SOURCE_CONSOLE_CONTROL_MSG,
            'CONSOLE_DESTINATION': DEST_CONSOLE_SOC_MSG,
            'CONSOLE_HEADER': THERMAL_IMAGE_USECASE_SETTING_MSG,
            'Addr': b'\x00',
            'data': b'\x05'
        },
        'TEC_OFF': {
            'CONSOLE_SOURCE': SOURCE_CONSOLE_CONTROL_MSG,
            'CONSOLE_DESTINATION': DEST_CONSOLE_SOC_MSG,
            'CONSOLE_HEADER': THERMAL_IMAGE_USECASE_SETTING_MSG,
            'Addr': b'\x00',
            'data': b'\x06'
        },
        'RAW_VIEW': {
            'CONSOLE_SOURCE': SOURCE_CONSOLE_CONTROL_MSG,
            'CONSOLE_DESTINATION': DEST_CONSOLE_SOC_MSG,
            'CONSOLE_HEADER': THERMAL_IMAGE_USECASE_SETTING_MSG,
            'Addr': b'\x00',
            'data': b'\x03'
        },
        'PATTERN_VIEW': {
            'CONSOLE_SOURCE': SOURCE_CONSOLE_CONTROL_MSG,
            'CONSOLE_DESTINATION': DEST_CONSOLE_SOC_MSG,
            'CONSOLE_HEADER': THERMAL_IMAGE_USECASE_SETTING_MSG,
            'Addr': b'\x00',
            'data': b'\x04'
        },
        'TRSM_REF_GUIDE_ON': {
            'CONSOLE_SOURCE': SOURCE_CONSOLE_CONTROL_MSG,
            'CONSOLE_DESTINATION': DEST_CONSOLE_SOC_MSG,
            'CONSOLE_HEADER': THERMAL_IMAGE_TRSM_GUIDE_MSG,
            'Addr': b'\x00',
            'data': b'\x01'
        },
        'TRSM_REF_GUIDE_OFF': {
            'CONSOLE_SOURCE': SOURCE_CONSOLE_CONTROL_MSG,
            'CONSOLE_DESTINATION': DEST_CONSOLE_SOC_MSG,
            'CONSOLE_HEADER': THERMAL_IMAGE_TRSM_GUIDE_MSG,
            'Addr': b'\x00',
            'data': b'\x00'
        },
        'TRSM_REF_GUIDE_UP': {
            'CONSOLE_SOURCE': SOURCE_CONSOLE_CONTROL_MSG,
            'CONSOLE_DESTINATION': DEST_CONSOLE_SOC_MSG,
            'CONSOLE_HEADER': THERMAL_IMAGE_TRSM_GUIDE_MSG,
            'Addr': b'\x01',
            'data': b'\x02'
        },
        'TRSM_REF_GUIDE_DOWN': {
            'CONSOLE_SOURCE': SOURCE_CONSOLE_CONTROL_MSG,
            'CONSOLE_DESTINATION': DEST_CONSOLE_SOC_MSG,
            'CONSOLE_HEADER': THERMAL_IMAGE_TRSM_GUIDE_MSG,
            'Addr': b'\x01',
            'data': b'\x03'
        },
        'TRSM_REF_GUIDE_LEFT': {
            'CONSOLE_SOURCE': SOURCE_CONSOLE_CONTROL_MSG,
            'CONSOLE_DESTINATION': DEST_CONSOLE_SOC_MSG,
            'CONSOLE_HEADER': THERMAL_IMAGE_TRSM_GUIDE_MSG,
            'Addr': b'\x01',
            'data': b'\x00'
        },
        'TRSM_REF_GUIDE_RIGHT': {
            'CONSOLE_SOURCE': SOURCE_CONSOLE_CONTROL_MSG,
            'CONSOLE_DESTINATION': DEST_CONSOLE_SOC_MSG,
            'CONSOLE_HEADER': THERMAL_IMAGE_TRSM_GUIDE_MSG,
            'Addr': b'\x01',
            'data': b'\x01'
        },
        'TRSM_REF_GUIDE_SAVE': {
            'CONSOLE_SOURCE': SOURCE_CONSOLE_CONTROL_MSG,
            'CONSOLE_DESTINATION': DEST_CONSOLE_SOC_MSG,
            'CONSOLE_HEADER': THERMAL_IMAGE_TRSM_GUIDE_MSG,
            'Addr': b'\x02',
            'data': b'\x00'
        },
        'TRSM_REF_APPLY': {
            'CONSOLE_SOURCE': SOURCE_CONSOLE_CONTROL_MSG,
            'CONSOLE_DESTINATION': DEST_CONSOLE_SOC_MSG,
            'CONSOLE_HEADER': THERMAL_IMAGE_TRSM_GUIDE_MSG,
            'Addr': b'\x03',
            'data': b'\x01'
        }


    }