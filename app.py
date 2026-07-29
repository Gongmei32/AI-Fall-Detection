from src.camera.webcam import Webcam


def main():

    camera = Webcam(0)
    camera.start()


if __name__ == "__main__":
    main()