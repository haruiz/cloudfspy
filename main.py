# @CloudPathFactory.register("x")
# class MyOwnSchemePathReader(CloudPath):
#     def __init__(self, cloud_path: str) -> None:
#         super().__init__(cloud_path)
#
#     def exists(self, *args, **kwargs):
#         return False  # implement your own logic here

# if __name__ == "__main__":
#     cloud_path = GenericPath("gs://gpr-studio-data/test/pictures/Archive.zip")
#     cloud_path2 = GenericPath("gs://gpr-studio-data/test/")
#     cloud_path3 = GenericPath("gs://gpr-studio-data/test/file.txt")
#     cloud_path4 = GenericPath("gs://gpr-studio-data/test/pictures/1")
#     local_path = GenericPath("data/file.txt")
#     local_path2 = GenericPath("x://data/file.txt")
#
#     paths = [
#         cloud_path,
#         cloud_path2,
#         cloud_path3,
#         cloud_path4,
#         local_path,
#         local_path2,
#     ]
#     for p in paths:
#         print(p.as_posix(), p.exists())

# local_file_data = local_path.read_bytes()
# cloud_file_data = cloud_path.read_bytes()
#
# from_path = GenericPath("/Users/haruiz/Desktop/test_Archive.zip")
# to_path = GenericPath("gs://gpr-studio-data/test/test_Archive.zip")
# from_path.upload_to(to_path)
# file_bytes = to_path.read_bytes()
# with open("test.zip", "wb") as f:
#     f.write(file_bytes)
# #
# from_path = GenericPath("gs://gpr-studio-data/test/test_Archive.zip")
# to_path = GenericPath("/Users/haruiz/Desktop/test_Archive-download.zip")
# from_path.download_to(to_path)
# file_bytes = to_path.read_bytes()
# with open("test.zip", "wb") as f:
#     f.write(file_bytes)
#
# for p in from_path.iterdir():
#     print(p.as_posix(), p.exists())
#
# folder = GenericPath("gs://gpr-studio-other/test/pictures/1")
# folder.mkdir(exist_ok=True, parents=True)
# cloud_file = folder.joinpath("20230918_104141.jpg")
# print(cloud_file.as_uri())
if __name__ == "__main__":
    import cloudfspy
    from cloudfspy import GenericPath as Path

    # set the cache folder
    cloudfspy.set_cache_folder("cache")
    cloudfspy.clear_cache_folder()
    
    from_path = Path("/Users/haruiz/Desktop/Archive.zip")
    to_path = Path("gs://gpr-studio-data/Archive.zip")

    from_path.upload_to(to_path)
    with open(to_path, "rb") as f:
        data = f.read()

    # print(urlparse("gs://gpr-studio-other").path.lstrip("/") == None)

    # local_file_path = "/Users/haruiz/Pictures/2023-09-18/20230918_104141.jpg"
    # cloud_file_path = "gs://gpr-studio-data/test/pictures/1/20230918_104141.jpg"
    # local_file = GenericPath(local_file_path)
    # cloud_file = GenericPath(cloud_file_path)
    #
    # local_file.upload_to(cloud_file_path)
    # cloud_file.download_to("20230918_104141.jpg")
    #
    # local_file_data = local_file.read_bytes()
    # cloud_file_data = cloud_file.read_bytes()
    #
    # from_path = GenericPath("/Users/haruiz/Desktop/test_Archive.zip")
    # to_path = "gs://gpr-studio-data/test/test_Archive.zip"
    # to_path = from_path.upload_to(to_path)
    # file_bytes = to_path.read_bytes()
    # with open("test.zip", "wb") as f:
    #     f.write(file_bytes)
    # #
    # from_path = GenericPath("gs://gpr-studio-data/test/test_Archive.zip")
    # to_path = "/Users/haruiz/Desktop/test_Archive-download.zip"
    # to_path = from_path.download_to(to_path)
    # file_bytes = to_path.read_bytes()
    # with open("test.zip", "wb") as f:
    #     f.write(file_bytes)

    # # cloud_file_path = "gs://gpr-studio-other/test/pictures/1/Archive.zip"
    #
    # cloud_file = GenericPath("gs://gpr-studio-data/dt_file.dt")
    # # cloud_file_bytes = cloud_file.read_bytes()
    #
    # with open(cloud_file, "rb") as f:
    #     data = f.read()
    #     print(len(data))

    # cloud_dir2 = GenericPath("gs://gpr-studio-data/test/pictures/1")

    # print(
    #     cloud_dir.joinpath("gs://gpr-studio-data/test/pictures/1").joinpath(
    #         "gs://gpr-studio-data/test/pictures/2"
    #     )
    # )

    # cloud_dir.mkdir(exist_ok=True, parents=True)
    # for p in cloud_dir.iterdir():
    #     print(p)

    # print(cloud_dir.parent.parent)
    # print(cloud_dir.exists())

    # cloud_dir.mkdir(exist_ok=True, parents=True)
    # cloud_dir.rmdir()

    # cloud_dir_parent = cloud_dir.parent
    # cloud_dir.mkdir(exist_ok=True, parents=True)
    # cloud_dir.rmdir()

    # cloud_dir = GenericPath("gs://gpr-studio_3/xx/1/2/3")
    # cloud_dir.mkdir(exist_ok=True, parents=True)
    # cloud_dir.rmdir()
    # cloud_dir.mkdir(exist_ok=True, parents=True)
    # cloud_dir.rmdir()

    # local_file = GenericPath(local_file_path)
    # cloud_file = local_file.upload_to(
    #     cloud_file_path, metadata={"description": "My lovely fun daughter"}
    # )
    # print(cloud_file.metadata)
    #
    # local_file = cloud_file.download_to("20230918_104141.jpg")
    # print(local_file.stat())
    # cloud_generic_file = GenericPath(cloud_file_path)
    # print(cloud_generic_file.stat())
    # with open(cloud_generic_file, "rb") as f:
    #     data = f.read()
    #     print(len(data))

    # uri = "https://drive.google.com/file/d/1A2B3C4D5E6F7G8H9I0J/view"
    # print(urlparse(uri))
