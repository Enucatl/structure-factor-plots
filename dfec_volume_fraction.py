import click
import csv
import numpy as np
import logging
import logging.config
from scipy import constants

import structure_factors.saxs
import structure_factors.lynch
from nist_lookup import xraydb_plugin as xdb
from structure_factors.logger_config import config_dictionary

from nist_lookup import xraydb_plugin as xdb

log = logging.getLogger()


@click.command()
@click.option("--energy", type=float, default=25,
              help="design energy of the interferometer [keV]")
@click.option("--grating_pitch", type=float, default=2e-6,
              help="pitch of G2 [m]")
@click.option("--intergrating_distance", type=float, default=12e-2,
              help="pitch of G2 [m]")
@click.option("--diameter", type=float, default=7.75e-6,
              help="diameter of the spheres [m]")
@click.option("--min_volume_fraction", type=float, default=0.01,
              help="min fraction of the total volume occupied by the spheres")
@click.option("--max_volume_fraction", type=float, default=0.6,
              help="max fraction of the total volume occupied by the spheres")
@click.option("--volume_fraction_steps", type=int, default=100,
              help="steps for the sampling of the volume fraction")
@click.option("--sphere_material", default="SiO2",
              help="chemical composition of the spheres")
@click.option("--sphere_density", type=float, default=2.0,
              help="density of the material of the spheres [g/cm³]")
@click.option("--background_material", default="C3H8O3",
              help="chemical composition of the background")
@click.option("--background_density", type=float, default=1.26,
              help="density of the material of the background [g/cm³]")
@click.option("--output", type=click.File("w"), default="-",
              help="output file for the csv data")
@click.option("--sampling", type=int, default=2048,
              help="""
              number of cells for the sampling of real and fourier space""")
@click.option("--verbose", is_flag=True, default=False)
def main(
        energy,
        grating_pitch,
        intergrating_distance,
        diameter,
        min_volume_fraction,
        max_volume_fraction,
        volume_fraction_steps,
        sphere_material,
        sphere_density,
        background_material,
        background_density,
        output,
        sampling,
        verbose
        ):
    if verbose:
        config_dictionary['handlers']['default']['level'] = 'DEBUG'
        config_dictionary['loggers']['']['level'] = 'DEBUG'
    logging.config.dictConfig(config_dictionary)
    wavelength = (constants.physical_constants["Planck constant in eV s"][0] *
                  constants.c / (energy * 1e3))
    volume_fractions = np.linspace(
        min_volume_fraction,
        max_volume_fraction,
        volume_fraction_steps
    )
    delta_sphere, beta_sphere, _ = xdb.xray_delta_beta(
        sphere_material,
        sphere_density,
        energy * 1e3)
    delta_background, beta_background, _ = xdb.xray_delta_beta(
        background_material,
        background_density,
        energy * 1e3)
    delta_chi_squared = (
        (delta_sphere - delta_background) ** 2 +
        (beta_sphere - beta_background) ** 2
    )

    autocorrelation_length = wavelength * intergrating_distance / grating_pitch
    real_space_sampling = np.linspace(
        -4 * autocorrelation_length,
        4 * autocorrelation_length,
        sampling,
        endpoint=False,
    )
    output_csv = csv.writer(output)
    output_csv.writerow(
        ["volume_fraction", "lynch", "saxs", "saxs hard spheres"]
    )
    for volume_fraction in volume_fractions:
        saxs = structure_factors.saxs.dark_field_extinction_coefficient(
            wavelength,
            grating_pitch,
            intergrating_distance,
            diameter,
            volume_fraction,
            delta_chi_squared,
            real_space_sampling
        )
        lynch = structure_factors.lynch.dark_field_extinction_coefficient(
            wavelength,
            grating_pitch,
            intergrating_distance,
            diameter,
            volume_fraction,
            delta_chi_squared,
        )
        saxs_hard_spheres = (
            structure_factors.saxs.dark_field_extinction_coefficient(
                wavelength,
                grating_pitch,
                intergrating_distance,
                diameter,
                volume_fraction,
                delta_chi_squared,
                real_space_sampling,
                structure_factors.saxs.hard_sphere_structure_factor
            ))
        output_csv.writerow([volume_fraction, lynch, saxs, saxs_hard_spheres])


if __name__ == "__main__":
    main()
