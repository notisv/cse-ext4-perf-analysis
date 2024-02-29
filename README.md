## About
The project was developed for the [Simulation and Modeling of Computational Systems](https://www.cs.uoi.gr/~gkappes/mye029) course @ [cse.uoi.gr](https://www.cs.uoi.gr/)

This project deals with the performance analysis of the journaled file system EXT4 in a VMware Workstation Player virtualization environment using Filebench.<br>

Specifically, one will benchmark the performance of various journaling modes used by the journal maintained by ext4 in a virtual machine intended to run in an environment serving dynamic websites.

The EXT4 file system is a journaled file system. It maintains a log file called a journal, in which it records the operations that are to be executed on the disk before they are actually performed.
The journal is particularly useful for recovering the system from errors in cases of abrupt system crashes. When a crash occurs, EXT4 examines the journal to repeat operations that did not manage to complete correctly.
The EXT4 journal supports three modes of operation: journaled, ordered, and writeback.

Filebench is a flexible benchmarking program for comparing the performance of file systems and storage systems. Its key feature is the inclusion of a number of artificial workloads that accurately represent specific categories of applications.
Additionally, it supports a high-level language called Workload Model Language (WML), which can be used to create new, customized workloads.
