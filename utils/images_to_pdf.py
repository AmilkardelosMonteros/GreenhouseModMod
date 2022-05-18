from PIL import Image
import glob

def create_pdf_images(name,path,folder):
    try:
        image_list = [Image.open(name).convert('RGB') for name in [f for f in glob.glob(path + '/' + folder + "/*.png")] ]
        im1    = image_list[0]
        images = image_list[1:]
        im1.save(path+'/reports/'+name+'.pdf',save_all=True, append_images=images)
    except:
        print('No se encontro el folder')
