from pymodm import MongoModel, fields


class Patient(MongoModel):
    """ Description of data to be stored for each patient

    This class derives from the pymodm.MongoModel class and is used to define
    the structure of a document in the database for this server. Each
    document will have four fields:

    mhrnumber (IntegerField) will be the patient's medical health record
        ID number. This is the primary key of the database.
    name (CharField) will be the patient's name.
    medimgs (DictField) will be a dict in which the keys are the medimg
        filenames, and the values are the b64_string variables
        containing the image bytes encoded as a base64 string.
    ecgimgs (DictField) will be a dict in which the keys are the ecgimg
        filenames, and the values are the b64_string variables containing
        the image bytes encoded as a base64 string.
    hrlist (ListField) will be a list containing int heart rates analyzed
        from uploaded ECG images.
    ecgimgtstamps (ListField) will be a list containing the timestamp and
        date at which the ecgimg (and resulting measured HR) was uploaded
        to the database.
    medimgtstamps (ListField) will be a list containing the timestamp and
        date at which the medimg was uploaded to the database.
    """
    mhrnumber = fields.IntegerField(primary_key=True)
    name = fields.CharField()
    medimgs = fields.DictField()
    ecgimgs = fields.DictField()
    hrlist = fields.ListField()
    ecgimgtstamps = fields.ListField()
    medimgtstamps = fields.ListField()
