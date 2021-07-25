import logging

from app.viewer import run

if __name__ == '__main__':
    logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-4s [%(asctime)s]  %(message)s',
                        level=logging.DEBUG)
    run()