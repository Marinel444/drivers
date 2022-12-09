import pytest
import argparse
from unittest import mock
from src.drivers_marinel import race_report


def test_log_file():
    with pytest.raises(FileNotFoundError) as e:
        race_report.parse_log_file('none')
    assert e.value.args[1] == 'No such file or directory'


def test_abbr_file():
    with pytest.raises(FileNotFoundError) as e:
        race_report.parse_abbreviations('none')
    assert e.value.args[1] == 'No such file or directory'


@mock.patch('argparse.ArgumentParser.parse_args', return_value=argparse.Namespace(desc=True, driver=None))
def test_desc_no_input(mock_args, capsys):
    race_report.main()
    output = capsys.readouterr()
    # print(output.out.strip())
    assert output.out.strip() == """№ | Code | Racer Name          | Team                          | Time
-------------------------------------------------------------------------------
19| LHM  | Lewis Hamilton      | MERCEDES                      | 0:06:47.540000
18| EOF  | Esteban Ocon        | FORCE INDIA MERCEDES          | 0:05:46.972000
17| SSW  | Sergey Sirotkin     | WILLIAMS MERCEDES             | 0:04:47.294000
16| DRR  | Daniel Ricciardo    | RED BULL RACING TAG HEUER     | 0:02:47.987000
15| KMH  | Kevin Magnussen     | HAAS FERRARI                  | 0:01:13.393000
-------------------------------------------------------------------------------
14| LSW  | Lance Stroll        | WILLIAMS MERCEDES             | 0:01:13.323000
13| MES  | Marcus Ericsson     | SAUBER FERRARI                | 0:01:13.265000
12| BHS  | Brendon Hartley     | SCUDERIA TORO ROSSO HONDA     | 0:01:13.179000
11| NHR  | Nico Hulkenberg     | RENAULT                       | 0:01:13.065000
10| CSR  | Carlos Sainz        | RENAULT                       | 0:01:12.950000
9 | PGS  | Pierre Gasly        | SCUDERIA TORO ROSSO HONDA     | 0:01:12.941000
8 | RGH  | Romain Grosjean     | HAAS FERRARI                  | 0:01:12.930000
7 | SPF  | Sergio Perez        | FORCE INDIA MERCEDES          | 0:01:12.848000
6 | CLS  | Charles Leclerc     | SAUBER FERRARI                | 0:01:12.829000
5 | FAM  | Fernando Alonso     | MCLAREN RENAULT               | 0:01:12.657000
4 | KRF  | Kimi Räikkönen      | FERRARI                       | 0:01:12.639000
3 | SVM  | Stoffel Vandoorne   | MCLAREN RENAULT               | 0:01:12.463000
2 | VBM  | Valtteri Bottas     | MERCEDES                      | 0:01:12.434000
1 | SVF  | Sebastian Vettel    | FERRARI                       | 0:01:04.415000"""


@mock.patch('argparse.ArgumentParser.parse_args', return_value=argparse.Namespace(desc=None, driver=None))
def test_desc_input(mock_args, capsys):
    race_report.main()
    output = capsys.readouterr()
    assert output.out.strip() == """№ | Code | Racer Name          | Team                          | Time
-------------------------------------------------------------------------------
1 | SVF  | Sebastian Vettel    | FERRARI                       | 0:01:04.415000
2 | VBM  | Valtteri Bottas     | MERCEDES                      | 0:01:12.434000
3 | SVM  | Stoffel Vandoorne   | MCLAREN RENAULT               | 0:01:12.463000
4 | KRF  | Kimi Räikkönen      | FERRARI                       | 0:01:12.639000
5 | FAM  | Fernando Alonso     | MCLAREN RENAULT               | 0:01:12.657000
6 | CLS  | Charles Leclerc     | SAUBER FERRARI                | 0:01:12.829000
7 | SPF  | Sergio Perez        | FORCE INDIA MERCEDES          | 0:01:12.848000
8 | RGH  | Romain Grosjean     | HAAS FERRARI                  | 0:01:12.930000
9 | PGS  | Pierre Gasly        | SCUDERIA TORO ROSSO HONDA     | 0:01:12.941000
10| CSR  | Carlos Sainz        | RENAULT                       | 0:01:12.950000
11| NHR  | Nico Hulkenberg     | RENAULT                       | 0:01:13.065000
12| BHS  | Brendon Hartley     | SCUDERIA TORO ROSSO HONDA     | 0:01:13.179000
13| MES  | Marcus Ericsson     | SAUBER FERRARI                | 0:01:13.265000
14| LSW  | Lance Stroll        | WILLIAMS MERCEDES             | 0:01:13.323000
15| KMH  | Kevin Magnussen     | HAAS FERRARI                  | 0:01:13.393000
-------------------------------------------------------------------------------
16| DRR  | Daniel Ricciardo    | RED BULL RACING TAG HEUER     | 0:02:47.987000
17| SSW  | Sergey Sirotkin     | WILLIAMS MERCEDES             | 0:04:47.294000
18| EOF  | Esteban Ocon        | FORCE INDIA MERCEDES          | 0:05:46.972000
19| LHM  | Lewis Hamilton      | MERCEDES                      | 0:06:47.540000"""


@mock.patch('argparse.ArgumentParser.parse_args', return_value=argparse.Namespace(desc=None, driver='KMH'))
def test_drivers_input(mock_args, capsys):
    race_report.main()
    output = capsys.readouterr()
    assert output.out.strip() == """№ | Code | Racer Name          | Team                          | Time
-------------------------------------------------------------------------------
15| KMH  | Kevin Magnussen     | HAAS FERRARI                  | 0:01:13.393000"""