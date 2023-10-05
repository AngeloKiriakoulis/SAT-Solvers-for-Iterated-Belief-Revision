# Belief Revision Algorithm, Using SAT solvers

This is an open-source application that uses SAT solvers to implement  belief revision in artificial intelligence systems. Belief revision is a process that allows the system to update its beliefs based on new information. This is an essential aspect of AI systems that deal with uncertain or incomplete information. This app uses Boolean satisfiability (SAT) solvers to perform the belief revision process efficiently.

## Table of Contents
- [Introduction](#introduction)
- [Installation](#installation)
- [Getting Started](#getting-started)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Introduction
This software implements a belief revision algorithm as described in my thesis. 
This belief revision algorithm is designed to answer to a given query (Q), while a  knowledge base (KB) is revised through new information (NI), while maintaining consistency. 

1. **Input Knowledge Base (KB):** The KB is a set of propositional clauses in CNF, represented as nested lists. It represents the existing knowledge or beliefs. For large KBs use files from the `RTI_k3_n100_m429` folder.

2. **New Information:** You can provide new information in the same CNF format, which will revise the existing knowledge base.

3. **Query :** You can also specify a query in CNF format. The algorithm can then check whether the updated knowledge base satisfies the query, helping you assess the implications of the new information.

4. **Belief Weights (W)** The hierarchy between beliefs to be revised is done using weights. The greater the weight of a proposal, the less likely it is to change.

5. **Belief Revision:** The algorithm was developed by Dr. Pavlos Peppas et. al. and it's part of the paper "Algorithmic Considerations of PD-Belief Revision" that is still in development.

6. **Result:** The result of the belief revision is True/False answer on whether or not the query comes as a logical consequence of the revision proccess happening in KB.

## Installation
To run this software, you'll need to follow the following steps.

1. Clone this repository to your local machine:
```
git clone https://github.com/AngeloKiriakoulis/SAT-Solvers-for-Iterated-Belief-Revision.git
```

2. Include all the needed dependencies by running:
``` 
pip install -r requirements.txt
```
## Getting Started

To get started with the belief revision algorithm, follow these steps:


1. After cloning this repository to your local machine, you will find sample input files in the `RTI_k3_n100_m429 ` directory. These files contain samples that can be used for the initial knowledge base (KB)

2. Choose one of the provided KB files by coping its path or create your own custom KB file in the same CNF format. You can use a text editor of your choice to create or modify these files.

3. Open a terminal or command prompt and navigate to the directory where you cloned the repository.

4. Choose the preferred version that you want to use (recommended v2.0) by running:
    ```
    cd v2.0
    ```
  
5. Run the programm:
    ```
    python belief_revision.py
    ```

6. Paste the KB file path to the terminal:
    ```
    Provide the initial Knowledge Base: ..\RTI_k3_n100_m429\RTI_k3_n100_m429_2.cnf
    ```
    or use your own:
    ```
    Provide the initial Knowledge Base: [[3, 5], [1, -2, 4, -5], [-3, 5], [3, 2], [-5, -2], [-4,-2]]
    ```
7. Define the New Information:
    ```
    Provide the New Information:[[-5,-3]]
    ```

8. Define the Query:
    ```
    Provide the Query: [[1],[-5]]
    ```

9. Define the Belief Weight Dictionary:   
    ```
    Provide the Belief Weights Dictionary: {1: 3, 2: 2, 3: 4, 4: 1, 5: 5}
    ```
10. The final results should look like this:
    ``` bash
    Q(0): [[-1, -2], [1, -2], [-1, 2]]
    S: [[-1, -2], [1, -2], [-1, 2]]
    T: [(frozenset({-1, -2}), []), (frozenset({1, -2}), []), (frozenset({2, -1}), [])]
    W: [[], [], []]
    E: ()
    R: [frozenset({-1, -2}), frozenset({1, -2}), frozenset({2, -1})]
    H: [[-2, -1], [2, -2], [1, -1]]
    False
    Execution time: 0.01611495018005371 seconds
    Memory usage: 87.8359375 MB
    ```

## Troubleshooting
If you encounter any issues while using this software, please refer to the [Troubleshooting Guide](troubleshooting.md) for common solutions. If your issue persists, feel free to [open an issue](https://github.com/AngeloKiriakoulis/SAT-Solvers-for-Iterated-Belief-Revision/issues) on GitHub.

## Contributing
Contributions are welcome! If you'd like to contribute to the development of this algorithm, please follow the [Contribution Guidelines](CONTRIBUTING.md).

## License
This software is distributed under the [License Name] license. See the [LICENSE](LICENSE) file for details.

---

Thank you for using our belief revision algorithm! If you have any questions or feedback, please don't hesitate to [contact us](angelokir86@gmail.com).

