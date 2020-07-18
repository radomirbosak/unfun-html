"""
Abstract class Gentor defining interface for generator-extractor classes
"""


class CannotExtractKernel(ValueError):
    """Given kernel cannot extract value"""


class Gentor:
    """
    Abstract class Gentor defining interface for generator-extractor classes
    """

    def traverse(self, soup):
        """
        Traverses the soup and generates kernels evaluatable by extract

        Args:
            soup: source document

        Returns: generator of kernels
        """
        raise NotImplementedError

    def extract(self, soup, kernel):
        """
        Interpret kernel for given soup

        Args:
            soup: source document
            kernel: recipe for extraction

        Returns: interpreted kernel

        Raises:
            CannotExtractKernel: No value can be extracted for this kernel and soup
        """
        raise NotImplementedError

    def semiwinners(self, soup, target):
        """
        Return winning kernels for one soup and one target

        Args:
            soup
            target
        """
        for kernel in self.traverse(soup):
            try:
                if self.extract(soup, kernel) == target:
                    yield kernel
            except CannotExtractKernel:
                pass

    def winners(self, dataset):
        """
        Return kernels which successfully extract the target for a single given dataset

        Args:
            dataset: list of tuples [(soup, target), ...]
        """
        semiwinner_list = []
        for soup, target in dataset:
            semi_winners = self.semiwinners(soup, target)
            semiwinner_list.append(list(semi_winners))

        if not semiwinner_list:
            return []

        # fetch kernels present in all datapoints
        winners = []
        for kernel in semiwinner_list[0]:
            if all(kernel in semi_winners for semi_winners in semiwinner_list):
                winners.append(kernel)
        return winners
