from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Optional, Union
from pydantic import BaseModel, Field
from LOOM.src.data_classes.LoomSet import LoomSet


class LoomInputParams(BaseModel):
    input_path: List[str] = Field(
        default=list,
        description="List of input file paths (1 for single file, >1 for multiple files)"
    )

    output_path: str = Field(
        default='output/', 
        description="Path to the output file or folder"
    )

class LoomAnalysis(ABC):
    """This abstract class implements a Loom Analysis.
    It fixes a common interface and workflow for all
    Loom analyses.

    Methods
    ----------
    get_input_params_model():
        Class abstract method which is responsible for
        defining and returning a validation model for the
        input parameters of the analysis. This method must
        be implemented by each derived analysis class.
    initialize(input_parameters: LoomInputParams):
        Class abstract method to set up analysis with validated
        parameters.
    read_input():
        Abstract method which is responsible for reading
        the input data for the analysis, p.e. Loom
        objects such as LoomSets. For more information,
        refer to its docstring.
    analyze():
        Abstract method which is responsible for performing
        the analysis on the input data. For more information,
        refer to its docstring.
    plot():
        Abstract method which is responsible for plotting
        the results of the analysis. For more information,
        refer to its docstring.
    write_output():
        Abstract method which is responsible for writing
        the output of the analysis. For more information,
        refer to its docstring.
    """

    def __init__(self):
        pass

    @classmethod
    @abstractmethod
    def get_input_params_model(cls) -> type:
        """This class method must be implemented by each
        derived analysis class. It must define and return
        a Pydantic model which will be used to validate
        the input parameters given to the analysis. The
        model must inherit from the LoomInputParams
        class."""
        pass

    @abstractmethod
    def initialize(self, input_parameters: LoomInputParams) -> None:
        """This method must be implemented by each derived
        analysis class. It is responsible for defining the
        instance attributes of the analysis class out of
        the given input parameters, which will abide by
        the model defined in the get_input_params_model()
        class method.
        Parameters
        ----------
        input_parameters: LoomInputParams
            The input parameters given to the analysis
        
        Returns
        ----------
        None
        """
        pass

    @abstractmethod
    def read_input(self) -> bool:
        """This method must be implemented by each derived
        analysis class. It is responsible for reading the
        input data for the analysis, p.e. Loom objects
        such as LoomSets. 
        
        Returns
        ----------
        bool
            True if the reading process ended normally, 
            False otherwise"""
        pass

    @abstractmethod
    def analyze(self) -> bool:
        """This method must be implemented by each derived
        analysis class. It is responsible for performing
        the analysis on the input data. 

        Returns
        ----------
        bool
            True if the analysis process ended normally,
            False otherwise
        """
        pass

    @abstractmethod
    def plot(self) -> bool:
        """This method must be implemented by each derived
        analysis class. It is responsible for plotting the
        results of the analysis.

        Returns
        ----------
        bool
            True if the plotting process ended normally,
            False otherwise
        """
        pass

    @abstractmethod
    def write_output(self) -> bool:
        """This method must be implemented by each derived
        analysis class. It is responsible for writing the
        output of the analysis. 
        
        Returns
        ----------
        bool
            True if the writing process ended normally,
            False otherwise
        """
        pass

    def execute(
            self,
            input_parameters: LoomInputParams) -> None:
        
        """Main execution method that runs the full LOOM 
        analysis pipeline."""

        self.initialize(input_parameters)
        self.read_input()
        self.analyze()
        self.plot()
        self.write_output()
