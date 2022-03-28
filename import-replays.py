import argparse
from pprint import pprint
from glob import glob
from shutil import copyfile, rmtree
import sys
import re
import os
import zipfile


# Examines how many replays there are in the replay folder currently
def get_current_replay_count(replay_folder):
    # Get highest replay ini, return its number
    current_replay_files = sorted(glob(os.path.join(replay_folder, 'round_*.ini')), reverse=True)
    if current_replay_files:
        return int(re.search('(\d{4})\.ini$', current_replay_files[0]).group(1))
    else: 
        return 0


# Reads out a value from an ini file
def get_ini_value(ini, key):
    with open(ini, 'r') as f:
        ini_text = f.read()
    match = re.search(f'{key} (.*)\n', ini_text)
    if match:
        return match.group(1)
    elif key in ['P1Name', 'P2Name']:
        # Local replays don't have player name fields. 
        return ""
    else:
        raise Exception(f"Failed to read key {key} from ini file {ini}!")


# Check a set of loose replay files
def validate_loose_files(ini_list, rnd_list, danisen):
    # Every .ini must have a corresponding .rnd, and vice versa
    for ini in ini_list:
        replay_code = re.search('(\d{4}).ini$', ini).group(1)
        if not any([re.search(f'round_{replay_code}\.rnd$', f) for f in rnd_list]):
            raise Exception(f"Found a round_{replay_code}.ini, but no round_{replay_code}.rnd!")
    for rnd in rnd_list: 
        replay_code = re.search('(\d{4}).rnd$', rnd).group(1)
        if not any([re.search(f'round_{replay_code}\.ini$', f) for f in ini_list]):
            raise Exception(f"Found a round_{replay_code}.rnd, but no round_{replay_code}.ini!")
    # Danisen sets: 5-9 replays only, enforces same players for each set
    if danisen:
        prompt_for_confirmation = False
        if len(ini_list) < 5: 
            print(f" Warning - not a valid danisen set, not enough replays for a FT5!")
            prompt_for_confirmation = True
        if len(ini_list) > 9: 
            print(f" Warning - not a valid danisen set, too many replays for a FT5!")
            prompt_for_confirmation = True
        if prompt_for_confirmation:
            confirmation = input("Is this ok? (y/n): ")
            if not confirmation or confirmation[0].lower() != "y":
                raise Exception(f"Invalid number of replays for a danisen set.")
        first_p1 = get_ini_value(ini_list[0], 'P1Name')
        first_p2 = get_ini_value(ini_list[0], 'P2Name')
        for ini in ini_list[1:]:
            p1 = get_ini_value(ini, 'P1Name')
            p2 = get_ini_value(ini, 'P2Name')
            if not ((p1 == first_p1 and p2 == first_p2) or (p1 == first_p2 and p2 == first_p1)):
                raise Exception(f"Not a valid danisen set - the two players don't stay the same!")


# Extract a zip file to the staging folder to work on its files temporarily
def extract_zip_file(zip_file, staging_folder):
    if not zipfile.is_zipfile(zip_file):
        raise Exception(f"not a valid zip file")
    with zipfile.ZipFile(zip_file, 'r') as zf:
        zf.extractall(path=staging_folder)


# Expand a zip file, and validate the replay files inside
# Returns a count of how many replays there are in total
def validate_zip_file(zip_file, staging_folder, danisen):
    extract_zip_file(zip_file, staging_folder)
    # Once extracted, we can treat it like a collection of loose files.
    ini_list = sorted(glob(os.path.join(staging_folder, '**', 'round_*.ini'), recursive=True))
    rnd_list = sorted(glob(os.path.join(staging_folder, '**', 'round_*.rnd'), recursive=True))
    if not ini_list or not rnd_list:
        raise Exception(f"I don't see any replay files in this zip: {zip_file}.")
    validate_loose_files(ini_list, rnd_list, danisen)
    return len(ini_list)


# Input file validation checking
def validate_input_files(input_files, ini_list, rnd_list, zip_list, staging_folder, replay_count, danisen):
    # Throw an error if there are too many replays already
    if replay_count >= 9998: 
        raise Exception("\nERROR: You already have too many replays (max is 9998).\n"
             "Delete some to make space before using this tool again.")

    # Check for empty input
    if not (ini_list or rnd_list or zip_list): 
        raise Exception("\nERROR: You didn't supply any replays to import!")

    # Check for any supplied invalid files 
    if len(ini_list) + len(rnd_list) + len(zip_list) != len(input_files): 
        raise Exception(f"\nERROR: found input file(s) that are not replays or zips.")

    # Validate loose replay files
    if ini_list:
        print(f"Validating loose replay files...", end='')
        validate_loose_files(ini_list, rnd_list, danisen)
        print(" OK")
    loose_replay_count = len(ini_list)

    # Validate each zip file (and count replays across all of them)
    zipped_replay_count = 0
    for zip_file in zip_list:
        short_name = re.search('([^\\\/]+)\.zip', zip_file).group(1)
        print(f"Validating zip file \"{short_name}\"...", end='')
        zipped_replay_count += validate_zip_file(zip_file, staging_folder, danisen)
        rmtree(staging_folder)
        print(" OK")

    # Make sure all these new replays will actually fit
    if replay_count + loose_replay_count + zipped_replay_count > 9998: 
        raise Exception("\nERROR: Adding these replays would push you past the max of 9998.\n" 
             "Delete some to make space, or don't import as many.")


# Imports a list of loose replay files, returns the new replay_count
def import_loose_files(ini_list, rnd_list, replay_folder, replay_count):
    for ini, rnd in zip(ini_list, rnd_list):
        replay_code = re.search('(\d{4}).ini$', ini).group(1)
        replay_count += 1
        copyfile(ini, os.path.join(replay_folder, f"round_{replay_count:04d}.ini"))
        copyfile(rnd, os.path.join(replay_folder, f"round_{replay_count:04d}.rnd"))
        print(f"Replay {replay_code} imported as {replay_count:04d}")
    return replay_count


# Imports all the replays inside a zip file
# Returns the new replay_count
def import_zip_file(zip_file, replay_folder, staging_folder, replay_count):
    extract_zip_file(zip_file, staging_folder)
    ini_list = sorted(glob(os.path.join(staging_folder, '**', 'round_*.ini'), recursive=True))
    rnd_list = sorted(glob(os.path.join(staging_folder, '**', 'round_*.rnd'), recursive=True))
    replay_count = import_loose_files(ini_list, rnd_list, replay_folder, replay_count)
    return replay_count


# Main function
if __name__ == "__main__":

    # This code is for running as a python script
    # parser = argparse.ArgumentParser()
    # parser.add_argument('--replayfolder', '-f', help='Path to the replays folder', required=True)
    # parser.add_argument('--inputfiles', '-i', nargs='+', help='list of input files to process', required=True)
    # parser.add_argument('--danisen', '-d', action='store_true', help='Danisen mode. 5-9 replays per zip only, enforce same players for each set')
    # args = parser.parse_args()
    # replay_folder = args.replayfolder
    # staging_folder = os.path.join(replay_folder, ".replay-importer-temp/")
    # input_files = sorted(args.inputfiles)
    # replay_count = get_current_replay_count(replay_folder)
    # original_replay_count = replay_count
    # danisen = args.danisen

    ## If I'm packaging this into an exe using pyinstaller, I will use this code
    ## to generate my arguments intead  
    replay_folder = re.fullmatch(r'(.*\\)(.*)\.exe', sys.argv[0]).group(1)
    input_files = sys.argv[1:]
    staging_folder = os.path.join(replay_folder, ".replay-importer-temp/")
    replay_count = get_current_replay_count(replay_folder)
    original_replay_count = replay_count
    danisen = False

    # Split up each input file by extension
    ini_list = list(filter(lambda f: re.search('round_\d{4}\.ini$', f), input_files))
    rnd_list = list(filter(lambda f: re.search('round_\d{4}\.rnd$', f), input_files))
    zip_list = list(filter(lambda f: re.search('\.zip$', f), input_files))

    # Do some validation on the input files first
    try:
        validate_input_files(input_files, ini_list, rnd_list, zip_list, staging_folder, replay_count, danisen)
    except Exception as err:
        print(f"\nError while validating input files:\n{err}")
        input("\nPress Enter to continue...")
        sys.exit()
    finally:
        if os.path.isdir(staging_folder):
            rmtree(staging_folder)

    # Import the new replays
    if ini_list: 
        print("\nImporting loose replays...")
        replay_count = import_loose_files(ini_list, rnd_list, replay_folder, replay_count)
    for zip_file in zip_list:
        short_name = re.search('([^\\\/]+)\.zip', zip_file).group(1)
        print(f"\nImporting zip file \"{short_name}\"...")
        try:
            replay_count = import_zip_file(zip_file, replay_folder, staging_folder, replay_count)
        except Exception as err:
            print(f"\nError while importing zip file \"{short_name}\":\n{err}")
            input("\nPress Enter to continue...")
            sys.exit()
        finally:
            if os.path.isdir(staging_folder):
                rmtree(staging_folder)

    # Print a summary of the result 
    print("\nSuccess!\n"
         f"First new replay:      {(original_replay_count + 1):04d}\n"
         f"# of replays imported: {(replay_count - original_replay_count):4d}")

    input("\nPress Enter to continue...")