
import argparse
import tempfile
import uuid
from scipy.io import wavfile
from slugify import slugify
import snowboy_model_config
from lib.snowboy_model import SnowboyPersonalEnroll, SnowboyTemplateCut

def check_enroll_output(enroll_ans):
    if enroll_ans == -1:
        raise Exception("Error initializing streams or reading audio data")
    elif enroll_ans == 1:
        raise Exception("Hotword is too long")
    elif enroll_ans == 2:
        raise Exception("Hotword is too short")

def get_model_name(name):
    return "{}_{}.pmdl".format(slugify(name), uuid.uuid1())


def main():
    parser = argparse.ArgumentParser(description='Command line client for generating snowboy personal model')
    parser.add_argument('-r1', '--record1', dest="record1", required=True, help="Record voice 1")
    parser.add_argument('-r2', '--record2', dest="record2", required=True, help="Record voice 2")
    parser.add_argument('-r3', '--record3', dest="record3", required=True, help="Record voice 3")
    parser.add_argument('-lang', '--language', default="en", dest="language", help="Language")
    parser.add_argument('-n', '--name', default="temp", dest="model_name", help="Personal model name")
    args = parser.parse_args()

    print("template cut")
    cut = SnowboyTemplateCut(
        resource_filename=snowboy_model_config.get_enroll_resource(args.language))

    out = tempfile.NamedTemporaryFile()
    model_path = str(out.name)

    print("personal enroll")
    enroll = SnowboyPersonalEnroll(
        resource_filename=snowboy_model_config.get_enroll_resource(args.language),
        model_filename=model_path)

    assert cut.NumChannels() == enroll.NumChannels()
    assert cut.SampleRate() == enroll.SampleRate()
    assert cut.BitsPerSample() == enroll.BitsPerSample()
    print("channels: %d, sample rate: %d, bits: %d" % (cut.NumChannels(), cut.SampleRate(), cut.BitsPerSample()))

    recording_set = [args.record1, args.record2, args.record3]
    for rec in recording_set:
        print("processing %s" % rec)
        _, data = wavfile.read(rec)
        data_cut = cut.CutTemplate(data.tobytes())
        enroll_ans = enroll.RunEnrollment(data_cut)

    check_enroll_output(enroll_ans)

    filename = get_model_name(args.model_name)
    print("saving file to %s" % filename)
    f = open(filename, "wb")
    f.write(open(out.name).read())
    f.close()
    print("finished")

if __name__ == "__main__":
    main()
