def teste(a, b, c=None):
    if c == None:
        return 'C é None meu fi'
    else:
        return 'Olha só, c não é mais none'


print(teste(1, 2))
print('-----------')
print(teste(1, 2, 3))
