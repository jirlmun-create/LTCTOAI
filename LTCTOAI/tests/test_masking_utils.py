import masking_utils

def test_mask_name():
    assert masking_utils.mask_name('김민수') == '김*수'
    assert masking_utils.mask_name('이수') == '이수'
    assert masking_utils.mask_name('박영수') == '박*수'

def test_mask_id():
    assert masking_utils.mask_id('900101-1234567') == '900101-*******'
    assert masking_utils.mask_id('800101-2345678') == '800101-*******'
