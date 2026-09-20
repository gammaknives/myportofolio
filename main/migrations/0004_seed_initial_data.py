from django.db import migrations
from datetime import datetime


def seed_data(apps, schema_editor):
    Project = apps.get_model("main", "Project")
    Experience = apps.get_model("main", "Experience")

    Project.objects.create(
        title="Boneka Bayangan",
        description="A short movie about a boy who loves to play with \"wayang\" (shadow puppets) and his struggles against people who ridicule traditional art. Competed and won in the FLS2N Short Movie Competition in 2024. I worked as a scriptwriter and a co-director for this project.",
        tags="Film, Directing, Scriptwriting",
        thumbnail="https://raw.githubusercontent.com/gammaknives/myportofolio/main/static/img/bonekabayangan.png",
        link="https://drive.google.com/file/d/1viMSeU9cqk5rn-jEcw4O9iR4YvgG2XaI/view?usp=sharing",
    )

    Project.objects.create(
        title="PiezoSun Path",
        description="A project integrating piezoelectric technology with solar panels to create an advanced, eco-friendly energy harvesting system. Competed and won on the National Instrumentation Festival 2025 issued by Institut Teknologi Sepuluh Nopember.",
        tags="Innovation, Hardware, Research",
        thumbnail="https://raw.githubusercontent.com/gammaknives/myportofolio/main/static/img/piezosunpath.png",
        link="https://canva.link/hjkmeknx1vl34hn",
    )

    Project.objects.create(
        title="Grantha Aksata",
        description="A short movie about a guy trying to find a reason why his friend committed suicide while he deals with his grief. Competed and won in the Elate 2024 Short Movie Competition. I worked as a scriptwriter.",
        tags="Film, Scriptwriting",
        thumbnail="https://raw.githubusercontent.com/gammaknives/myportofolio/main/static/img/granthaaksata.png",
        link="https://drive.google.com/file/d/1UnCCTH9X8L8-OOokqTSrUD2n-wjTqYGF/view?usp=sharing",
    )

    Project.objects.create(
        title="Karya Tulis: Strategi Pemasaran Kedai \"Kopi Tuku\" dalam Menjaga Loyalitas Konsumen Remaja Putri Jakarta Selatan",
        description="A written work about marketing strategies implemented by \"Kopi Tuku\" in South Jakarta to maintain customer loyalty among teenage girls. Used as a final project / paper for SMA Kolese Gonzaga.",
        tags="Writing, Research",
        thumbnail="https://raw.githubusercontent.com/gammaknives/myportofolio/main/static/img/kartul.png",
        link="https://docs.google.com/document/d/1SGV-7-ITVS_FhYDvMqOJ3r0dihZWQ48PErTfy5GV-Dw/edit?usp=sharing",
    )

    Project.objects.create(
        title="Messenger",
        description="A short movie about a guy struggling to keep his letter writing business afloat as he tries to find innovations to keep his business relevant in the modern world. An extracurricular project for Sinematografi Gonzaga. I worked as a director and scriptwriter for this project.",
        tags="Film, Directing, Scriptwriting",
        thumbnail="https://raw.githubusercontent.com/gammaknives/myportofolio/main/static/img/messenger.png",
        link="https://drive.google.com/file/d/1mBaSstUoP9bYTZRxyp9qfy0JpRGbpgJH/view?usp=sharing",
    )

    Project.objects.create(
        title="Tiup Lilinnya",
        description="A short movie about a guy feeling lonely on his birthday and his struggles to find a way to celebrate it. A small project used as a presentation for a class assignment. I worked as a director and scriptwriter for this project.",
        tags="Film, Directing, Scriptwriting",
        thumbnail="https://raw.githubusercontent.com/gammaknives/myportofolio/main/static/img/tiuplilinnya.png",
        link="https://drive.google.com/file/d/1J6LdHUDafBiVb5Zy6VhWHOrT_-gFuXgI/view?usp=sharing",
    )

    Experience.objects.create(
        title="Gonzaga Festival Short Movie Competition Committee",
        description="Helped with planning and managing the competition from start to finish",
        category="volunteer",
        started_at=datetime(2024, 1, 1),
        ended_at=datetime(2024, 12, 31),
    )

    Experience.objects.create(
        title="FLS2N Short Movie 1st Runner Up Winner",
        description='Won the FLS2N short movie competition as a scriptwriter and co-director for the movie "Boneka Bayangan"',
        category="volunteer",
        started_at=datetime(2024, 1, 1),
        ended_at=datetime(2024, 12, 31),
    )

    Experience.objects.create(
        title="Camastiore Elate Short Movie 2nd Place Winner",
        description='Won the Camastiore Elate short movie competition as a scriptwriter for the movie "Grantha Aksata"',
        category="volunteer",
        started_at=datetime(2024, 1, 1),
        ended_at=datetime(2024, 12, 31),
    )

    Experience.objects.create(
        title="Instrumentation Festival 3rd Runner Up Winner",
        description="Won the national Instrumentation Festival issued by Institut Teknologi Sepuluh Nopember by creating and presenting the PiezoSun Path innovation",
        category="research",
        started_at=datetime(2025, 1, 1),
        ended_at=datetime(2025, 12, 31),
    )

    Experience.objects.create(
        title="Member of Sinematografi UI Production Division",
        description="Active member of the production team for the UKM Sinematografi UI creating short movies and hosting workshops",
        category="volunteer",
        started_at=datetime(2025, 1, 1),
        ended_at=None,
    )


def remove_data(apps, schema_editor):
    Project = apps.get_model("main", "Project")
    Experience = apps.get_model("main", "Experience")
    Project.objects.all().delete()
    Experience.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_alter_experience_started_at'),
    ]

    operations = [
        migrations.RunPython(seed_data, remove_data),
    ]
