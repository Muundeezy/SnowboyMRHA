
import argparse
import tempfile
import uuid
from scipy.io import wavfile
from pmdl import snowboy_pmdl_config
from pmdl.snowboy_pmdl import SnowboyPersonalEnroll, SnowboyTemplateCut
import glob
import os

def check_enroll_output(enroll_ans):
    if enroll_ans == -1:
        raise Exception("Error initializing streams or reading audio data")
    elif enroll_ans == 1:
        raise Exception("Hotword is too long")
    elif enroll_ans == 2:
        raise Exception("Hotword is too short")


def main():
    parser = argparse.ArgumentParser(description='Command line client for generating snowboy personal model')
    parser.add_argument('-rD', '--recording-dir', dest="recordDir", help="The directory containing the recording wav files")
    parser.add_argument('-r1', '--record1', dest="record1", help="Record voice 1")
    parser.add_argument('-r2', '--record2', dest="record2", help="Record voice 2")
    parser.add_argument('-r3', '--record3', dest="record3", help="Record voice 3")
    parser.add_argument('-n', '--name', dest="model_name", help="Personal model name")
    parser.add_argument('-lang', '--language', default="en", dest="language", help="Language")
    args = parser.parse_args()

    if args.recordDir:
        recording_set = glob.glob(os.path.join(args.recordDir + '/*.wav'))
        if len(recording_set) < 3:
            raise exit('The directory needs to contain at least 3 wav files')
    elif args.record1 and args.record2 and args.record3:
        recording_set = [args.record1, args.record2, args.record3]
    else:
        raise exit('Please specify either three wav file or a directory containing the wav files.')

    print("template cut")
    cut = SnowboyTemplateCut(
        resource_filename=snowboy_pmdl_config.get_enroll_resource(args.language))

    out = tempfile.NamedTemporaryFile()
    model_path = str(out.name)

    print("personal enroll")
    enroll = SnowboyPersonalEnroll(
        resource_filename=snowboy_pmdl_config.get_enroll_resource(args.language),
        model_filename=model_path)

    assert cut.NumChannels() == enroll.NumChannels()
    assert cut.SampleRate() == enroll.SampleRate()
    assert cut.BitsPerSample() == enroll.BitsPerSample()
    print("channels: %d, sample rate: %d, bits: %d" % (cut.NumChannels(), cut.SampleRate(), cut.BitsPerSample()))

    if recording_set:
        for rec in recording_set:
            print("processing %s" % rec)
            _, data = wavfile.read(rec)
            data_cut = cut.CutTemplate(data.tobytes())
            enroll_ans = enroll.RunEnrollment(data_cut)

        check_enroll_output(enroll_ans)

        filename = args.model_name
        print("saving file to %s" % filename)
        f = open(filename, "wb")
        f.write(open(out.name).read())
        f.close()
        print("finished")
    else:
        print('No wav files found')

if __name__ == "__main__":
    main()
