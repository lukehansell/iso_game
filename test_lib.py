import lib
class TestLib:
    def test_should_convert_back_and_forth(self):
        grid_ref = (11, 45)
        result = lib.iso_to_grid_ref(lib.grid_ref_to_iso(grid_ref))

        assert result == grid_ref