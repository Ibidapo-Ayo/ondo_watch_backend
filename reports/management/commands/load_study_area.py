import json
from pathlib import Path

from django.contrib.gis.geos import GEOSGeometry, MultiPolygon
from django.core.management.base import BaseCommand, CommandError

from reports.models import StudyArea


class Command(BaseCommand):

    help = "Load a study area boundary from a GeoJSON file."

    def add_arguments(self, parser):
        parser.add_argument(
            "geojson_file",
            type=str,
            help="Path to the GeoJSON study area file.",
        )

        parser.add_argument(
            "--name",
            required=True,
            help="Name of the study area.",
        )

        parser.add_argument(
            "--state",
            default="",
            help="State associated with the study area.",
        )

        parser.add_argument(
            "--country",
            default="Nigeria",
            help="Country associated with the study area.",
        )

        parser.add_argument(
            "--description",
            default="",
            help="Description of the study area.",
        )

    def handle(self, *args, **options):

        geojson_file = Path(options["geojson_file"])

        if not geojson_file.exists():
            raise CommandError(
                f"GeoJSON file not found: {geojson_file}"
            )

        try:
            with geojson_file.open(
                "r",
                encoding="utf-8",
            ) as file:
                geojson_data = json.load(file)

        except json.JSONDecodeError:
            raise CommandError(
                "The file is not valid JSON/GeoJSON."
            )

        geometry = geojson_data.get("geometry")

        if geometry is None:

            features = geojson_data.get("features", [])

            if len(features) != 1:
                raise CommandError(
                    "GeoJSON must contain exactly one feature."
                )

            geometry = features[0].get("geometry")

        if geometry is None:
            raise CommandError(
                "No geometry was found in the GeoJSON file."
            )

        try:
            spatial_geometry = GEOSGeometry(
                json.dumps(geometry)
            )

        except Exception as error:
            raise CommandError(
                f"Could not read geometry: {error}"
            )

        if spatial_geometry.srid is None:
            spatial_geometry.srid = 4326

        if spatial_geometry.srid != 4326:
            spatial_geometry.transform(4326)
            
        if spatial_geometry.empty:
            raise CommandError(
            "Study area geometry is empty."
         )

        if not spatial_geometry.valid:
            raise CommandError(
            f"Study area geometry is invalid: "
            f"{spatial_geometry.valid_reason}"
         )   

        if spatial_geometry.geom_type == "Polygon":
            spatial_geometry = GEOSGeometry(
                json.dumps({
                    "type": "MultiPolygon",
                    "coordinates": [
                        spatial_geometry.coords
                    ],
                })
            )
            spatial_geometry.srid = 4326

        if spatial_geometry.geom_type != "MultiPolygon":
            raise CommandError(
                "Study area must be a Polygon or MultiPolygon."
            )

        study_area, created = StudyArea.objects.update_or_create(
            name=options["name"],
            defaults={
                "state": options["state"],
                "country": options["country"],
                "description": options["description"],
                "boundary": spatial_geometry,
                "active": True,
            },
        )

        if created:
            self.stdout.write(
                self.style.SUCCESS(
                    f"Study area created: {study_area.name}"
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    f"Study area updated: {study_area.name}"
                )
            )