from src.lib import grid_ref_to_iso, iso_to_grid_ref

class TestLib:
    def test_should_convert_back_and_forth(self):
        grid_ref = (11, 45)
        (iso_x, iso_y) = grid_ref_to_iso(grid_ref)
        result = iso_to_grid_ref((iso_x, iso_y))

        assert result == grid_ref