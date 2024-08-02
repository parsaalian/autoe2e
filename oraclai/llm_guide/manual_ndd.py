VISIT_ONCE = [
    # pet clinic
    'http:\/\/localhost:4200\/petclinic\/owners\/\d+',
    'http:\/\/localhost:4200\/petclinic\/vets\/\d+\/edit',
    'http:\/\/localhost:4200\/petclinic\/pettypes\/\d+\/edit',
    'http:\/\/localhost:4200\/petclinic\/specialties\/\d+\/edit',
    # saleor
    'http:\/\/localhost:3000\/default-channel\/products\/.+'
]

NEVER_VISIT = [
    # saleor
    'http:\/\/localhost:3000\/default-channel\/products$',
    'http:\/\/localhost:3000\/default-channel\/collections\/.+',
    'http:\/\/localhost:3000\/default-channel\/categories\/.+'
]

FORBIDDEN_ACTIONS = [
    # pet clinic
    (
        'http://localhost:4200/petclinic/owners/add',
        '//BODY/APP-ROOT[1]/DIV[2]/APP-OWNER-ADD[1]/DIV[1]/DIV[1]/FORM[1]/DIV[7]/DIV[1]/BUTTON[2]'
    ),
    (
        'http://localhost:4200/petclinic/owners/1/pets/add',
        '//BODY/APP-ROOT[1]/DIV[2]/APP-PET-ADD[1]/DIV[1]/DIV[1]/FORM[1]/DIV[6]/DIV[1]/BUTTON[2]'
    ),
    (
        'http://localhost:4200/petclinic/pets/1/visits/add',
        '//BODY/APP-ROOT[1]/DIV[2]/APP-VISIT-ADD[1]/DIV[1]/DIV[1]/FORM[1]/DIV[2]/DIV[1]/BUTTON[2]'
    ),
    (
        'http://localhost:4200/petclinic/vets/add',
        '//BODY/APP-ROOT[1]/DIV[2]/APP-VET-ADD[1]/DIV[1]/DIV[1]/FORM[1]/DIV[5]/DIV[1]/BUTTON[2]'
    ),
    (
        'http://localhost:4200/petclinic/pettypes',
        '//BODY/APP-ROOT[1]/DIV[2]/APP-PETTYPE-LIST[1]/DIV[1]/DIV[1]/DIV[1]/APP-PETTYPE-ADD[1]/DIV[1]/DIV[1]/FORM[1]/DIV[2]/DIV[1]/BUTTON[1]'
    ),
    (
        'http://localhost:4200/petclinic/specialties',
        '//BODY/APP-ROOT[1]/DIV[2]/APP-SPECIALTY-LIST[1]/DIV[1]/DIV[1]/DIV[1]/APP-SPECIALTY-ADD[1]/DIV[1]/DIV[1]/FORM[1]/DIV[2]/DIV[1]/BUTTON[1]'
    )
]
