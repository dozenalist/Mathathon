# Computations and certificates

The [local outputs](../Main/ResearchSnapshot/local/outputs/) include the Heule
coordinates, union certificate, no-forcing witnesses, and independent verifiers.
The [local work directories](../Main/ResearchSnapshot/local/work/) preserve the
graph, honeycomb, quotient, amplifier, and SAT-certificate audits.

Run the import checks from the repository root with Node.js:

```sh
node HadwigerNelson/Main/verify-snapshot.mjs
```

The original exact union checker can also be run directly:

```sh
node HadwigerNelson/Main/ResearchSnapshot/local/outputs/Verify-HeuleUnion.mjs
```

It reconstructs every pair of the 1,048-vertex translated union using exact
multiquadratic arithmetic and verifies the supplied five-colouring. The
553-vertex standalone checker uses Python 3:

```sh
python HadwigerNelson/Main/ResearchSnapshot/local/outputs/Verify-HeuleNoForcing.py
```

The snapshot check also validates all 34 five-colourings in each no-forcing
certificate and the distinct vertex signatures. These are statements about the
specific finite graphs. Periodic quotients, honeycomb exclusions, and sampled
direction families retain their stated restrictions.

Latest remote experiments are under
[remote/supervisor](../Main/ResearchSnapshot/remote/supervisor/) and
[remote/results](../Main/ResearchSnapshot/remote/results/). A remote result's
presence in the archive does not itself confer independent verification.
