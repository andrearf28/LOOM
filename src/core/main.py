# src/core/main.py

import pathlib
import argparse # To handle command line arguments
import LOOM.src.core.utils as lcu
import LOOM.src.exceptions as le

def main():
    
    """
    Main entry point to run LOOM optical analyses.

    This script:
    - Validates the analysis folder structure.
    - Parses command-line arguments (global and analysis-specific).
    - Dynamically imports and instantiates analysis classes.
    - Validates input parameters via each analysis’s parameter model.
    - Executes analyses sequentially.

    Exceptions are raised if these conditions are not met.
    
    """

    # Verify that the current working directory is a valid analysis folder
    try:
        lcu.analysis_folder_meets_requirements()
    except Exception as caught_exception:
        print(caught_exception)
        raise le.LoomBaseException(
            le.GenerateExceptionMessage(
                1, 
                'main()', 
                reason="Either you are not running from the analysis "
                "folder, or you are but your analysis folder does "
                "not meet the minimal requirements set by "
                "lcu.analysis_folder_meets_requirements()."
            )
        )
    
    # Create the argument parser to handle general command-line options.
    # These include global flags like --verbose, --parameters_file, etc.
    parser = argparse.ArgumentParser(description="LOOM Analyses main program")
    
    lcu.add_arguments_to_parser(parser)
    
    # Parse known args; unknown args are saved in remaining_args to be
    # forwarded later to the specific analysis classes.
    args, remaining_args = parser.parse_known_args()

    # Get the ordered list of analyses to run
    analyses = lcu.get_ordered_list_of_analyses(args, remaining_args, args.verbose)

    for i in range(len(analyses)):

        if args.verbose:
            print(f"In function main(): Running analysis stage {i+1} of {len(analyses)}")
        
        # Get the name of the current analysis folder 
        analysis_folder_name = pathlib.Path.cwd().name 

        # Dynamically build the import command to load the analysis class
        import_command = (
            f"from LOOM.src.analysis."
            f"{analysis_folder_name}.{analyses[i]['name']} "
            f"import {analyses[i]['name']}"
        )

        try:
            exec(import_command)
            
        except Exception as e:
            raise le.LoomBaseException(
                le.GenerateExceptionMessage(
                    2,
                    'main()',
                    reason="An exception occurred while executing the "
                    f"following import statement: \n \t {import_command}"
                    f"\n The caught exception message is: \n \t {e} \n"
                    "If the analysis module was not found, make sure to "
                    "add an __init__.py file to the analysis folder and "
                    "re-install LOOM."
                )
            )

        if args.verbose:
            print(
                "In function main(): Initializing an object of "
                f"type {analyses[i]['name']}"
            )
        
        # Instantiate the analysis class
        current_analysis = locals()[analyses[i]['name']]()
        
        # Build the dictionary of input parameters for the current analysis.
        parameters_to_deliver = lcu.build_parameters_dictionary(
            parameters_file_name = lcu.empty_string_to_None(
                analyses[i]['parameters_file']
            ),
            parameters_shell_string = lcu.empty_string_to_None(
                analyses[i]['overwriting_parameters']
            ),
            prioritize_string_parameters = True,
            verbose = args.verbose
        )

        # This ensures all required parameters are present and correctly typed.
        validated_parameters = \
            locals()[analyses[i]['name']].get_input_params_model()(
                **parameters_to_deliver
            )

        if args.verbose:
            print(
                "In function main(): Validated the following "
                f"input parameters: \n \n {validated_parameters}"
                "\n"
            )
        # Run the analysis with the validated parameters
        current_analysis.execute(validated_parameters)

if __name__ == "__main__":
    main()
