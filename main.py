from fractals import fractal, random_fractal

def run():
    file_name = input('Please type the name of your file:')
    choice = input('Print a random pattern (Yes/No?):').lower()
    file_name = f'svgs\\{file_name}.svg'
    if choice in {'y', 'yes'}:
        dwg = random_fractal(file_name)
    else:
        dwg = fractal(file_name)
    dwg.save()

if __name__ == '__main__':
    run()
